# État de l'art

Légende de vérification : ✅ vérifié dans une source consultée pendant la création du dépôt ; ⚠ de mémoire ou vu seulement dans des résultats de recherche, à vérifier avant de citer dans un rapport.

## 1. Que veut dire « résoudre » les échecs ?

Victor Allis (1994) distingue trois niveaux (⚠ de mémoire) :

| Niveau | Définition | Aux échecs |
|---|---|---|
| Ultra-faible | valeur de la position initiale (gain Blancs, nulle, gain Noirs), sans stratégie | non résolu |
| Faible | valeur + stratégie pour l'obtenir depuis la position initiale | non résolu |
| Forte | valeur de toute position légale | ≤ 7 pièces (et une partie des 8 pièces) |

Ce projet vise un objet voisin mais **hors classification** : une « résolution pratique », où l'on arrête l'exploration quand un camp a un avantage jugé décisif (seuil d'oracle). Ce n'est pas une preuve au sens strict ; la question est de mesurer à quel point c'est fiable.

## 2. Ordres de grandeur

| Quantité | Valeur | Source |
|---|---|---|
| Positions légales | ≈ 4,82 × 10⁴⁴ (± 0,03), estimation de John Tromp | ⚠ résultat de recherche citant Tromp |
| Arbre de jeu (nombre de Shannon) | ≈ 10¹²⁰ | ⚠ Wikipédia « Shannon number » |
| Positions à 8 pièces | 38 176 306 877 748 245 ≈ 3,8 × 10¹⁶ | ✅ Wikipédia « Endgame tablebase », blog Lichess Op1 |
| Tables 8 pièces complètes au format Syzygy | ≈ 2 Po (estimation) | ✅ Wikipédia « Endgame tablebase » |

Conséquence : on ne résoudra pas les échecs par énumération. Toute approche réaliste repose sur (a) des tables de finales exactes pour peu de pièces, (b) de la recherche, (c) des heuristiques pour couper des branches, d'où l'intérêt d'un seuil d'oracle.

## 3. Tables de finales : chronologie

| Année | Événement |
|---|---|
| 1980–1990 | Premières tables à 5 pièces (Ken Thompson), ⚠ de mémoire |
| ~2000 | Tables Nalimov (DTM, jusqu'à 6 pièces), ⚠ de mémoire |
| 2012 | Lomonosov : 7 pièces en DTM, 140 To, par Vladimir Makhnychev et Victor Zakharov (Université d'État de Moscou) ✅. Hors ligne depuis une attaque par rançongiciel en 2021 ✅ |
| avril 2013 | Syzygy (Ronald de Man) ✅ |
| 2018 | Syzygy 7 pièces achevées : 18,4 To en DTZ ✅ |
| depuis 2021 | Travaux sur les 8 pièces, toujours en cours en 2026 ✅ |
| 2025 | Op1 : table partielle à 8 pièces (Marc Bourzutschky, mise en ligne par Niklas Fiekas sur Lichess) ✅ |

Plus long mat forcé connu avec ≤ 7 pièces : 549 coups (DTM), découvert en 2012 pendant le calcul de Lomonosov ✅.

## 4. Syzygy en détail

Tailles du format DTZ (✅ Wikipédia) :

| Pièces | Taille |
|---|---|
| 3 | 25,8 Ko |
| 4 | 4,3 Mo |
| 5 | 979,6 Mo |
| 6 | 160,2 Go |
| 7 | 18,4 To |

Les tables WDL sont plus petites que les DTZ ✅ (elles tiennent sur un SSD ; la page consultée ne donne pas de tailles par nombre de pièces).

Points pratiques (✅ documentation python-chess) :

- Deux familles de fichiers : WDL (extension `.rtbw` ⚠) et DTZ (`.rtbz` ⚠).
- WDL à 5 valeurs du point de vue du camp au trait : `2` gain, `1` gain « cursed » (nulle par la règle des 50 coups), `0` nulle, `-1` perte « blessed », `-2` perte.
- DTZ50'' avec arrondi : la valeur peut être décalée d'un demi-coup, ce qui compte dans les positions proches de la nulle aux 50 coups.
- **Pas de positions avec droits de roque.**
- Sonder une position peut nécessiter les tables des matériels atteignables par capture ou promotion (par exemple les tables à 5 pièces pour sonder une position à 6).
- Sécurité : vérifier les sommes de contrôle des fichiers, des fichiers malveillants peuvent provoquer un déni de service.
- Stockfish sonde Syzygy via l'option UCI `SyzygyPath` ⚠ de mémoire.

## 5. Métriques

| Métrique | Contenu | Remarque |
|---|---|---|
| WDL | gain / nul / perte (5 valeurs avec règle des 50 coups) | la plus petite, suffisante pour calibrer un seuil |
| DTZ | coups avant un coup « zéroant » (capture ou coup de pion) | sert à respecter la règle des 50 coups |
| DTM | coups avant le mat | optimale en longueur, très volumineuse |
| DTC | coups avant le mat, ou une capture/promotion gagnante | DTC ≤ DTM ✅ ; utilisée par Op1 ✅ |

## 6. Les 8 pièces

- Total : ≈ 3,8 × 10¹⁶ positions ✅ ; tables complètes estimées à ≈ 2 Po au format Syzygy ✅.
- **Op1** ✅ (blog Lichess) : positions à 8 pièces avec **au moins une paire de pions opposés bloqués** (un pion blanc et un pion noir sur la même colonne, face à face), jusqu'à 6 pions. Exclut les finales où un camp n'a qu'un seul pion (par exemple KQRBNPvKP). 120 configurations de paires (15 par colonne × 8). ≈ 5,0 × 10¹⁴ positions légales, soit ≈ 1,3 % des positions à 8 pièces. Données : 63 TiB, métrique DTC. Un peu plus de la moitié des finales à 8 pièces rencontrées sur Lichess en 2025 en relèvent. Accès : téléchargement, API tablebase de Lichess, analyse Lichess, interface `op1-tables.info` (en cours).
- Pour les pistes de Marc Bourzutschky sur les 8 pièces : entretien ChessBase « 8 piece endgame tablebases first findings and interview » ⚠ (vu dans les résultats de recherche, non lu).

## 7. Corrections à apporter aux notes de départ

| Dans les notes | Précision |
|---|---|
| « de Man (2013) & Guo (2018) : inventeurs des tables Syzygy (6 et 7 pièces) » | Syzygy est l'œuvre de Ronald de Man (avril 2013). Les tables 7 pièces ont été achevées en 2018 ✅. Le rôle de Bojun Guo dans ce calcul n'apparaît pas dans les pages consultées : ⚠ à vérifier avant de le citer. |
| « Op1 … finales à 8 pièces sans pions et paires de pions bloqués » | Op1 couvre les positions avec **au moins une paire de pions bloqués** ✅. Ce n'est pas une base « sans pions ». |
| « En 2026, de nombreuses portions de tables à 8 pièces » | Une seule table partielle publiée est documentée ici (Op1, ≈ 1,3 % des positions) ; l'effort global reste en cours ✅. |
| « Le code Syzygy en C est intégré à Stockfish » | Stockfish intègre une version adaptée du code de sondage ⚠ de mémoire. Voir `docs/RESSOURCES.md`. |

## 8. Autres jeux résolus (pour situer l'effort) ⚠ de mémoire

- Dames anglaises : résolu (faiblement), match nul, Schaeffer et al., 2007.
- Puissance 4 : victoire du premier joueur, Allis et Allen, 1988.
- Awari : résolu (fortement), nul, Romein et Bal, 2003.

Les échecs ont un espace d'états très supérieur à celui des dames (≈ 5 × 10²⁰ positions ⚠), d'où l'intérêt d'une approche partielle.

## 9. Ce que cela implique pour le projet

1. **Vérité terrain disponible jusqu'à 7 pièces** (et 8 partiellement via Op1 par l'API Lichess) : on peut mesurer objectivement la fiabilité d'un seuil d'oracle.
2. **Le solveur lui-même est validable** : sur ≤ 6 pièces il doit retrouver les verdicts Syzygy.
3. **Au-delà de 8 pièces, aucune vérité terrain** : toute extrapolation du seuil est une hypothèse, à signaler comme telle dans le rapport.
