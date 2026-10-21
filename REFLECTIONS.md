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
