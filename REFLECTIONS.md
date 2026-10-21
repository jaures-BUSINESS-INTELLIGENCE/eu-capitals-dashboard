## Before building anything: weather vs. CO2
<!-- Avant de construire quoi que ce soit : météo contre CO2 -->

I would choose the closest destination. I would almost ignore the weather,
because a short trip means low CO2 and it is also cheaper and faster.
<!-- Je choisirais la destination la plus proche. J'ignorerais presque la météo,
parce qu'un trajet court veut dire peu de CO2, et qu'il est aussi moins cher et plus rapide. -->
## Stage 1: acquisition reliability
With 26 separate connections there are 26 chances for a failure, so the
chance that the whole operation succeeds goes down (if each call works 97%
of the time, all 26 work only about 45% of the time). Also, the calls come
from the same shared IP, so the server can slow or block it after a few
requests. One batched request has only one chance to fail, and it can be
retried as a whole.
<!-- Avec 26 connexions séparées, il y a 26 risques d'échec, donc le taux de
réussite de l'opération baisse (si chaque appel marche 97 % du temps, les 26
ne marchent ensemble que ~45 % du temps). Les appels viennent aussi de la
même adresse partagée, donc le serveur peut la ralentir ou la bloquer.
Une seule requête n'a qu'un risque d'échec et peut être réessayée en entier. -->
## Stage 1: provenance (CO2 factor)
Before publishing for real travelers, I would replace the rounded 0.15 value
with the current official figure (for example from DEFRA or ADEME). I would
write the source and the year next to it on the page, and I would check it
again every year, because these values change.
<!-- Avant de publier pour de vrais voyageurs, je remplacerais la valeur
arrondie 0,15 par le chiffre officiel actuel (par exemple DEFRA ou ADEME).
J'écrirais la source et l'année à côté sur la page, et je le revérifierais
chaque année, car ces valeurs changent. -->

## Stage 2: relative vs. absolute
No, the real temperature of an average capital would not change. A
temperature is a measurement, and adding a new city does not change the
weather in the other cities. But its score would change. normalize() uses
the best and the worst value in the list. For example, with temperatures
10, 15 and 20, the city at 15 gets a score of 0.5. If I add a city at 0
degrees, the city at 15 gets 0.75. The temperature is the same, but the
score is different. So a KPI depends on choices we make (which cities are in
the list, how we scale the values), while a measurement does not. This is
the idea of CM2: a KPI is built by us, it is not a neutral fact.
<!-- Non, la vraie température d'une capitale moyenne ne changerait pas.
Une température est une mesure, et ajouter une ville ne change pas le temps
des autres villes. Mais son score changerait. normalize() utilise la
meilleure et la pire valeur de la liste. Par exemple, avec des températures
de 10, 15 et 20, la ville à 15 a un score de 0,5. Si j'ajoute une ville à
0 degré, la ville à 15 a 0,75. La température est la même, mais le score est
différent. Donc un KPI dépend de choix que nous faisons (quelles villes
sont dans la liste, comment on met les valeurs à l'échelle), alors qu'une
mesure n'en dépend pas. C'est l'idée du CM2 : un KPI est construit par
nous, ce n'est pas un fait neutre. -->
## Stage 3: prediction
My prediction is Brussels. It is the capital closest to Paris, so it should
have the best CO2 score, and CO2 counts for half of the final score.
<!-- Ma prédiction est Bruxelles. C'est la capitale la plus proche de Paris,
donc elle devrait avoir le meilleur score CO2, et le CO2 compte pour la moitié
du score final. -->
## Stage 6: was my prediction right?
No. I predicted Brussels, but Madrid is first and Brussels is only fifth.
Brussels has the best CO2 score (1.0), as I expected, but its weather score
is very low (0.234) this week. Since weather counts for half of the final
score, Madrid wins with a good weather score (0.803) and a good CO2 score
(0.706). What surprised me was the weather data and the formula: I thought
the distance would be enough, but the 50/50 formula punishes bad weather.
<!-- Non. J'avais prédit Bruxelles, mais Madrid est première et Bruxelles
seulement cinquième. Bruxelles a le meilleur score CO2 (1,0), comme prévu,
mais son score météo est très bas (0,234) cette semaine. Comme la météo
compte pour la moitié du score final, Madrid gagne avec un bon score météo
(0,803) et un bon score CO2 (0,706). Ce qui m'a surpris, ce sont les
données météo et la formule : je pensais que la distance suffirait, mais la
formule 50/50 pénalise le mauvais temps. -->
## Stage 6: monitoring
The one thing a visitor can look at is the line "Data last updated ..." at
the bottom of the page. The workflow runs every Monday, so if the date is
more than a week or two old, something is wrong. But this signal is not
good enough on its own: the visitor has to notice it, and many will not
look at the date. I would add a visible warning on the page when the data
is more than 10 days old, and an email alert when the workflow fails.
GitHub also stops scheduled workflows after 60 days without activity, and
nobody would see that on the page.
<!-- La seule chose qu'un visiteur peut regarder est la ligne « Data last
updated ... » en bas de la page. Le workflow tourne chaque lundi, donc si la
date a plus d'une ou deux semaines, il y a un problème. Mais ce signal ne
suffit pas seul : le visiteur doit le remarquer, et beaucoup ne regarderont
pas la date. J'ajouterais un avertissement visible sur la page quand les
données ont plus de 10 jours, et une alerte par e-mail quand le workflow
échoue. GitHub arrête aussi les workflows programmés après 60 jours sans
activité, et personne ne le verrait sur la page. -->
