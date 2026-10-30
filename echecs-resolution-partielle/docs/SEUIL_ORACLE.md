# Le seuil de l'oracle

C'est la question centrale du projet : **à partir de quel score Stockfish peut-on considérer qu'une position est « gagnée » pour arrêter la recherche, et avec quelle fiabilité ?**

## 1. L'échelle de score n'est pas du matériel

Dans les versions récentes de Stockfish, le score affiché est **normalisé** : ✅ **+1,00 correspond à 50 % de probabilité de gagner** (parties de self-play du test de longue durée de Fishtest), quelle que soit la position. La conversion s'appuie sur une loi logistique :

```
win_rate(x)  = 1 / (1 + exp(−(x − a) / b))
loss_rate(x) = win_rate(−x)
draw_rate(x) = 1 − win_rate(x) − loss_rate(x)
```

où `a` et `b` dépendent de la phase de jeu (matériel ou numéro de coup). Source : dépôt `official-stockfish/WDL_model` ✅.

Conséquences :

- **« +10 » n'est pas « 10 pions d'avance »** : c'est un score très loin de l'équilibre, donc une probabilité de gain très proche de 1.
- **« Environ une dame d'avance » (9 points de matériel) n'est pas « +9,00 »** : le score Stockfish dépend de la position, pas du total des valeurs de pièces. À mesurer, pas à supposer.
- **L'échelle a changé selon les versions** (la normalisation a évolué entre Stockfish 16.1 et 17 d'après le dépôt WDL_model ✅). Toujours **fixer et noter la version de Stockfish** dans les résultats.

Option UCI `UCI_ShowWDL` : Stockfish affiche alors les probabilités victoire/nulle/défaite à côté du score ✅. python-chess expose cette information via `PovScore.wdl()` ⚠ (à vérifier dans la documentation de la version utilisée).

## 2. Définitions

Pour une famille de positions `P` et un seuil `T` :

- **Prédicat de l'oracle** : `D_T(p) = (|score(p)| ≥ T)`, avec le signe indiquant le camp gagnant.
- **Vérité** : `G(p) = (WDL Syzygy = ±2)`, c'est-à-dire un gain *sans* l'aide de la règle des 50 coups (les gains « cursed » ne comptent pas).
- **Précision** : `P(G | D_T)`. Mesure les **faux décisifs** (le point critique : couper une branche à tort).
- **Rappel** : `P(D_T | G)`. Mesure les gains manqués (moins grave : la recherche continue plus longtemps).
- **Taux de faux décisifs** : `1 − précision`.

Ce qu'on cherche : le **plus petit T** tel que la précision atteigne un plateau proche de 1 pour la famille étudiée. Plus T est petit, plus on coupe tôt (efficace) ; plus il est grand, plus on est sûr (coûteux).

## 3. Protocole de calibration

1. Choisir une famille de matériel (`KQvK`, `KQRvKR`, `KRPvKR`, …).
2. Tirer `N` positions légales aléatoires (`calibrate.py`, graine fixée).
3. Pour chaque position : score Stockfish (profondeur ou nombre de nœuds **fixés**) et WDL Syzygy.
4. Pour chaque T d'une grille : précision, rappel, nombre de faux décisifs.
5. Répéter en changeant la profondeur, le matériel, puis le nombre de pièces.

```bash
python -m echecs_solver.calibrate --tb data/syzygy --material KQRvKR -n 1000 --depth 14 \
    --thresholds 100 300 500 900 1500 3000
```

Grille de départ suggérée (centipions) : 100, 300, 500, 700, 900, 1200, 1500, 2000, 3000.

## 4. Quelle taille d'échantillon ?

Si on observe **0 faux décisif sur n positions**, une borne haute à 95 % du taux de faux décisifs est environ `3 / n` (« règle des trois »). Pour garantir un taux inférieur à 0,1 %, il faut ≈ 3 000 positions décisives sans erreur. Pour une estimation plus fine, utiliser un intervalle de Wilson plutôt que `p ± 1,96 √(p(1−p)/n)`, peu fiable près de 0 ou 1.

Attention à l'**échantillonnage uniforme** : les positions aléatoires sont souvent absurdes (pièces en prise, roi en échec évident). Prévoir un second jeu de positions plus réalistes : positions issues de parties, ou positions atteintes par la recherche elle-même.

## 5. Où le seuil peut se tromper

| Cas | Pourquoi l'oracle se trompe |
|---|---|
| Forteresses | grand avantage matériel mais nulle par blocage |
| Zugzwang / positions bloquées | l'évaluation statique ne voit pas la nulle |
| Mauvais fou + pion de la colonne a/h | nulle malgré un pion ou un fou d'avance |
| Gains « cursed » | gain théorique mais nul à cause des 50 coups |
| Horizon | un échec perpétuel ou un mat au-delà de la profondeur d'analyse |
| Nombre de pièces élevé | pas de vérité terrain au-delà de 7 pièces (8 partiellement) |

Chaque catégorie doit être cherchée explicitement dans les faux décisifs trouvés : un faux décisif est une position à étudier à la main.

## 6. Variantes de seuil à comparer

| Variante | Définition | Avantage | Inconvénient |
|---|---|---|---|
| Score absolu | `|cp| ≥ T` | simple | échelle dépendante de la version |
| Probabilité de gain | `P(gain) ≥ p` (WDL de Stockfish) | interprétable, plus stable | dépend du modèle WDL |
| Matériel | avance ≥ 9 points | intuitif (« une dame ») | ignore la position (fortresses, pions passés) |
| Mixte | matériel **et** score | filtre les faux positifs matériels | deux paramètres |

## 7. Deux sens de « gagné »

1. **Théorique** : le camp avantagé gagne avec un jeu parfait (vérité Syzygy).
2. **Pratique** : un joueur occasionnel bat un grand joueur depuis cette position (objectif initial du projet).

La calibration mesure le sens 1. Pour le sens 2, une expérience complémentaire est possible : jouer des parties Stockfish à force limitée (options `UCI_LimitStrength` et `UCI_Elo` ⚠ de mémoire, plage d'Elo selon la version) pour le « joueur occasionnel », contre Stockfish à pleine force pour le « grand joueur », depuis des positions de score donné, et mesurer le score selon T. À noter : l'avantage théorique et l'avantage pratique ne se confondent pas.

## 8. Hypothèses à tester

- **H1** : la précision croît avec T puis atteint un plateau proche de 1.
- **H2** : le seuil du plateau dépend du matériel (finales de pions ≠ finales de pièces lourdes).
- **H3** : à profondeur d'analyse faible, le plateau est plus haut (l'oracle se trompe plus).
- **H4** : un seuil mesuré à 5–6 pièces ne se transpose pas tel quel à 8 pièces et plus.

Ce sont des hypothèses, pas des résultats.
