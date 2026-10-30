# Méthodes

## 1. Analyse rétrograde (construction des tables)

Principe : partir des positions terminales (mat) et remonter vers l'arrière.

```
Entrée : une classe de matériel M (ex. KQvK)
1. Indexer toutes les positions de M (en exploitant les symétries)
2. Positions où le camp au trait est mat  → « perdu en 0 »
3. Pour n = 1, 2, … :
     a. position où UN coup mène à « perdu en n−1 » pour l'adversaire → « gagné en n »
     b. position dont TOUS les coups mènent à des positions « gagnées » → « perdu »
4. Positions jamais étiquetées → nulles
Captures et promotions : consulter les tables des matériels plus petits, déjà calculées.
```

Points délicats :

- **Indexation** : numéroter chaque position de façon compacte (placements de pièces, symétries du plateau, positions illégales exclues). C'est ce qui rend les tables calculables.
- **Dépendances entre matériels** : calculer KQvK avant KQRvK, etc. (ordre par nombre de pièces).
- **Règle des 50 coups** : DTZ et WDL à 5 valeurs plutôt que DTM pur (voir `ETAT_DE_L_ART.md`).
- **Compression** : Syzygy compresse fortement (compression par paires récursives, ⚠ de mémoire) pour tenir sur disque.
- **Coût** : mémoire et disque dominent, pas le calcul (de 160 Go à 18,4 To de 6 à 7 pièces).

Pour ce projet, on **n'a pas besoin de recalculer** les tables : on les sonde.

## 2. Recherche vers l'avant

| Technique | Idée | Usage ici |
|---|---|---|
| Minimax / alpha-bêta | explorer l'arbre en élaguant les branches inutiles | ordre des coups et élagage = vitesse |
| Table de transposition | mémoriser les positions déjà vues (hachage de Zobrist) | déjà présent (`cache`), sans historique |
| Approfondissement itératif | profondeur croissante, meilleur ordre des coups | permet de limiter le temps |
| Proof-number search (Allis) | développer d'abord le nœud le plus « facile à prouver » | adapté aux preuves de gain (⚠ de mémoire) |
| df-pn (Nagai) | variante en profondeur d'abord, moins gourmande en mémoire | ⚠ de mémoire |
| MCTS | simulations aléatoires guidées | ne **prouve** rien, hors sujet pour une preuve |

La recherche de preuve d'un gain est un **arbre ET/OU** : OU aux nœuds du camp qui veut gagner (un coup suffit), ET aux nœuds de l'adversaire (toutes ses défenses doivent échouer). C'est la structure de `Solver.white_wins`.

## 3. Approche hybride du dépôt

Feuilles possibles d'un nœud :

1. **Mat / pat / matériel insuffisant** : verdict exact.
2. **Table de finales** (≤ `tb_max_pieces`, sans roque) : verdict exact.
3. **Oracle** : `score ≥ T` (en centipions, vue des Blancs) : verdict **heuristique**.
4. **Profondeur épuisée** : « non prouvé » (traité comme faux).

Une preuve qui n'utilise que les feuilles 1 et 2 est une vraie preuve. Une preuve qui utilise des feuilles de type 3 est **conditionnelle** : valable si l'oracle ne se trompe pas aux feuilles. Amélioration à prévoir : compter séparément les feuilles de chaque type dans le résultat, pour mesurer la part de « confiance » dans chaque verdict.

## 4. Choisir des sous-problèmes

Commencer là où la vérité terrain existe (Syzygy) pour valider le solveur, puis monter :

| Famille | Exemples | Intérêt |
|---|---|---|
| 3 à 4 pièces | KQvK, KRvK, KPvK | tests de bon sens |
| 5 pièces | KQvKR, KRPvKR, KBNvK | finales célèbres (Lucena, Philidor), mats longs |
| 6 pièces | KQPvKQ, KRRvKR | premières vraies difficultés de recherche |
| 7 pièces | KQRvKRB, … | vérité terrain locale lourde ; API Lichess possible |
| avec « dame d'avance » | KQPPvKPP, KQRvKRR | le cas visé par le projet |

## 5. Pistes d'optimisation

- **Ordre des coups** : captures, échecs, promotions d'abord (gros gain pour `any`).
- **Cache persistant** (SQLite ou LMDB) pour ne pas recalculer entre exécutions.
- **Parallélisme** : un processus Stockfish par cœur, partage de la table de transposition par la racine.
- **Symétries** : canonicaliser la position (miroir horizontal quand il n'y a pas de roque) avant de consulter le cache.
- **Budget d'oracle** : fixer la profondeur ou le nombre de nœuds Stockfish, et les consigner pour la reproductibilité.
- **Coupe asymétrique** : n'appeler l'oracle qu'aux nœuds où le camp au trait est le camp attaquant, ou à profondeur paire (à tester).

## 6. Règles qui compliquent la preuve

| Règle | Effet |
|---|---|
| 50 coups | un gain « cursed » n'est pas un gain ; l'oracle ne le voit pas toujours |
| Répétition | une preuve par recherche doit éviter les cycles ; le cache sans historique les ignore |
| Roque | non sondable dans Syzygy ; position à traiter par recherche |
| Prise en passant | gérée par Syzygy et python-chess |
