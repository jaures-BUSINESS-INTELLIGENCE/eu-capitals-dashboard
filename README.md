# EU capitals — sustainable vacation dashboard 
<!-- Tableau de bord des capitales de l'UE pour des vacances durables (TD1) -->

Which EU capital offers the best weather next week while producing the
least CO2 to get there from Le Mans?
<!-- Quelle capitale de l'UE offre le meilleur temps la semaine prochaine tout
en produisant le moins de CO2 pour y aller depuis Le Mans ? -->

**Live page:** https://jaures-business-intelligence.github.io/capitals-dashboard/
<!-- Page en ligne -->

## How it works
<!-- Comment ça marche -->

1. A GitHub Action runs every Monday at 06:00 UTC (or manually).
   <!-- Une GitHub Action se lance chaque lundi à 06:00 UTC (ou à la main). -->
2. `scripts/fetch_and_score.py` gets a 7-day forecast for all capitals from
   the Open-Meteo API in one single request.
   <!-- Le script récupère les prévisions à 7 jours de toutes les capitales via
   l'API Open-Meteo, en une seule requête. -->
3. It computes the distance from Le Mans, the round-trip CO2 (0.15 kg per km),
   and scores from 0 to 1 for temperature, sunshine, rain and CO2.
   <!-- Il calcule la distance depuis Le Mans, le CO2 aller-retour (0,15 kg par
   km), et des scores de 0 à 1 pour la température, le soleil, la pluie et le CO2. -->
4. The final score is 50% weather and 50% CO2.
   <!-- Le score final vaut 50 % météo et 50 % CO2. -->
5. The result is saved in `docs/data/rankings.json` and committed, so every
   past ranking stays in the Git history.
   <!-- Le résultat est enregistré dans docs/data/rankings.json et commité, donc
   chaque ancien classement reste dans l'historique Git. -->
6. `docs/index.html` (GitHub Pages) reads this file and shows a bar chart of
   the ranking and a scatter plot of weather vs. CO2.
   <!-- docs/index.html (GitHub Pages) lit ce fichier et affiche un graphique en
   barres du classement et un nuage de points météo / CO2. -->

## Repository structure
<!-- Structure du dépôt -->

- `data/capitals.csv` — the capitals and their coordinates
- `scripts/fetch_and_score.py` — fetches the weather and computes the scores
- `docs/` — the web page and the generated `rankings.json`
- `.github/workflows/update-data.yml` — the weekly automation
- `REFLECTIONS.md` — my written answers to the TD questions

## Limits
<!-- Limites -->

- The CO2 factor (0.15 kg/km) is a rounded value and must be checked against
  an official source (DEFRA, ADEME) before real use.
  <!-- Le facteur CO2 est une valeur arrondie, à vérifier avec une source officielle. -->
- Distances are straight lines, not real flight routes.
  <!-- Les distances sont à vol d'oiseau, pas les vraies routes aériennes. -->
- The scores are relative: they depend on the list of cities being compared.
  <!-- Les scores sont relatifs : ils dépendent de la liste des villes comparées. -->
- Flight price is not part of the score.
  <!-- Le prix du vol ne fait pas partie du score. -->

## Data source
<!-- Source des données -->

Weather: [Open-Meteo](https://open-meteo.com) (free, no key needed).
