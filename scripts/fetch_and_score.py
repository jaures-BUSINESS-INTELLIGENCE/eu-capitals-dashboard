import csv, json, math, time
import requests

# Point de départ : Paris (latitude, longitude)
PARIS_LAT, PARIS_LON = 48.8566, 2.3522
# kg de CO2 par km parcouru (valeur arrondie, à vérifier/mettre à jour)
EMISSIONS_FACTOR_KG_PER_KM = 0.15

def haversine_km(lat1, lon1, lat2, lon2):
    # Distance en km entre deux points GPS, en ligne droite sur la sphère terrestre
    r = 6371  # rayon de la Terre en km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))

def fetch_weather_batch(lats, lons, retries=4, backoff=5):
    """One request for every destination at once, instead of one connection per
    capital. This isn't just fewer lines -- it fixes a real failure mode: 26
    separate TLS handshakes from a shared GitHub Actions runner IP is 26 separate
    chances for a connection to hang or get throttled, and in testing it reliably
    failed partway through (a handful of capitals fetched fine, then the rest
    started timing out on every retry). One request means one connection, and it
    is also roughly 100x faster in practice (all 26 forecasts typically arrive in
    well under a second)."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        # Toutes les latitudes/longitudes dans une seule requête, séparées par des virgules
        "latitude": ",".join(str(v) for v in lats),
        "longitude": ",".join(str(v) for v in lons),
        # Ce qu'on demande : température max, pluie, durée d'ensoleillement par jour
        "daily": "temperature_2m_max,precipitation_sum,sunshine_duration",
        "timezone": "auto", "forecast_days": 7,
    }
    last_error = None
    for attempt in range(1, retries + 1):  # jusqu'à 4 essais
        try:
            resp = requests.get(url, params=params, timeout=(15, 30))
            resp.raise_for_status()  # erreur si le serveur répond mal
            data = resp.json()
            return data if isinstance(data, list) else [data]
        except requests.exceptions.RequestException as e:
            last_error = e
            print(f"  batch weather fetch attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                time.sleep(backoff * attempt)  # on attend un peu plus à chaque échec
    raise RuntimeError(f"Open-Meteo unreachable after {retries} attempts") from last_error

def normalize(values, invert=False):
    # Ramène les valeurs sur une échelle 0-1 (le pire = 0, le meilleur = 1)
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.5 for _ in values]  # toutes égales : on met 0.5 pour éviter une division par zéro
    scaled = [(v - lo) / (hi - lo) for v in values]
    # invert=True : plus la valeur est petite, meilleur est le score (pluie, CO2)
    return [1 - s for s in scaled] if invert else scaled

def main():
    # 1) Lire la liste des capitales
    with open("data/capitals.csv") as f:
        rows = list(csv.DictReader(f))

    # 2) On retire Paris : on ne recommande pas d'aller là où l'on est déjà
    dest_rows = [row for row in rows if row["capital"] != "Paris"]
    lats = [float(row["lat"]) for row in dest_rows]
    lons = [float(row["lon"]) for row in dest_rows]

    # 3) Une seule requête météo pour toutes les capitales
    print(f"Fetching weather for {len(dest_rows)} capitals in a single batched request...")
    weather = fetch_weather_batch(lats, lons)
    # Sécurité : autant de réponses que de capitales, sinon on s'arrête
    if len(weather) != len(dest_rows):
        raise RuntimeError(
            f"Open-Meteo returned {len(weather)} results for {len(dest_rows)} "
            "requested locations -- refusing to guess the pairing."
        )
    print(f"Received {len(weather)} results")

    # 4) Calculer, pour chaque capitale, distance, CO2 et météo moyenne
    destinations = []
    for row, lat, lon, wx in zip(dest_rows, lats, lons, weather):
        distance_km = haversine_km(PARIS_LAT, PARIS_LON, lat, lon)
        daily = wx["daily"]
        avg_temp = sum(daily["temperature_2m_max"]) / len(daily["temperature_2m_max"])
        total_precip = sum(daily["precipitation_sum"])
        avg_sunshine = sum(daily["sunshine_duration"]) / len(daily["sunshine_duration"])
        destinations.append({
            "country": row["country"], "capital": row["capital"],
            "lat": lat, "lon": lon,
            "distance_km": round(distance_km, 1),
            # aller-retour : 2 x distance x facteur d'émission
            "co2_kg_roundtrip": round(2 * distance_km * EMISSIONS_FACTOR_KG_PER_KM, 1),
            "avg_max_temp": round(avg_temp, 1),
            "total_precip_mm": round(total_precip, 1),
            "avg_sunshine_s": round(avg_sunshine, 0),
        })

    # 5) Transformer chaque mesure en score de 0 à 1
    temp_scores = normalize([d["avg_max_temp"] for d in destinations])
    sun_scores = normalize([d["avg_sunshine_s"] for d in destinations])
    rain_scores = normalize([d["total_precip_mm"] for d in destinations], invert=True)
    co2_scores = normalize([d["co2_kg_roundtrip"] for d in destinations], invert=True)

    # 6) Scores finaux : météo = moyenne (température, soleil, pluie) ; final = moitié météo, moitié CO2
    for d, t, s, rn, c in zip(destinations, temp_scores, sun_scores, rain_scores, co2_scores):
        d["weather_score"] = round((t + s + rn) / 3, 3)
        d["co2_score"] = round(c, 3)
        d["final_score"] = round((d["weather_score"] + d["co2_score"]) / 2, 3)

    # 7) Trier du meilleur au moins bon
    destinations.sort(key=lambda d: d["final_score"], reverse=True)

    # 8) Écrire le résultat, avec la date de génération
    output = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "emissions_factor_kg_per_km": EMISSIONS_FACTOR_KG_PER_KM,
        "destinations": destinations,
    }
    with open("docs/data/rankings.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"Wrote {len(destinations)} destinations to docs/data/rankings.json")

if __name__ == "__main__":
    main()
