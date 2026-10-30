# Résolution partielle du jeu d'échecs

Résoudre les échecs « pour de vrai » est hors de portée : on estime à environ 4,8 × 10⁴⁴ le nombre de positions légales. Ce projet explore une **résolution pratique** : explorer l'arbre de jeu à partir d'une position donnée et **s'arrêter dès qu'un camp a un avantage décisif**, soit prouvé exactement par une table de finales (Syzygy), soit jugé suffisant par un oracle (Stockfish), par exemple environ une dame d'avance, de quoi permettre à un joueur occasionnel de battre un grand joueur.

> **Statut : base de départ.** Les tests unitaires utilisent un oracle factice (matériel seul). L'intégration avec un vrai Stockfish et de vraies tables Syzygy est à valider sur ta machine.

## L'idée en un schéma

```
position
   │
   ▼
table de finales (≤ 7 pièces, sans roque) ? ── oui ──► verdict EXACT (gain / nul / perte)
   │ non
   ▼
oracle Stockfish : |score| ≥ T ? ───────────── oui ──► verdict « décisif » (heuristique)
   │ non
   ▼
développer les coups, profondeur − 1
   OU pour le camp qui veut gagner (un coup suffit)
   ET pour l'adversaire (toutes ses défenses doivent échouer)
```

Les deux questions de recherche : **quelle valeur de T ?** et **quelle est la fiabilité d'un tel seuil ?** (voir [`docs/SEUIL_ORACLE.md`](docs/SEUIL_ORACLE.md)).

## Niveaux de « résolution »

| Niveau | Signification | Échecs |
|---|---|---|
| Ultra-faible | connaître la valeur théorique de la position initiale | non résolu |
| Faible | valeur + stratégie depuis la position initiale | non résolu |
| Forte | valeur de **toute** position légale | résolu seulement pour ≤ 7 pièces, partiellement pour 8 |
| Pratique (ce projet) | verdict « avantage décisif » sous un seuil d'oracle, validé par des tables | à explorer |

## Démarrage rapide

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q                      # tests, sans Stockfish ni Syzygy

# 1. Installer Stockfish (binaire dans le PATH) et noter sa version
# 2. Télécharger les tables Syzygy 3-4-5 pièces (~1 Go) dans data/syzygy/  → docs/RESSOURCES.md
# 3. Calibrer le seuil sur un matériel donné :
python -m echecs_solver.calibrate --tb data/syzygy --material KQRvKR -n 300
```

Utilisation en Python :

```python
import chess, chess.syzygy
from echecs_solver.oracle import Oracle
from echecs_solver.solver import Solver

with Oracle("stockfish", depth=14) as oracle, chess.syzygy.open_tablebase("data/syzygy") as tb:
    solver = Solver(oracle, tb, threshold=900)  # seuil en centipions (échelle Stockfish)
    print(solver.white_wins(chess.Board("4k3/8/8/8/8/8/8/Q3K3 w - - 0 1"), depth=2))
```

## Structure du dépôt

```
src/echecs_solver/
  oracle.py       enveloppe Stockfish (score en centipions, vue des Blancs)
  solver.py       arbre ET/OU borné : table de finales → oracle → développement
  calibrate.py    seuil T vs vérité Syzygy (précision, rappel, faux « décisifs »)
tests/            tests avec un oracle factice
data/syzygy/      tables de finales (ignorées par git)
docs/
  ETAT_DE_L_ART.md  niveaux de résolution, chiffres, tables de finales, 8 pièces
  METHODES.md       analyse rétrograde, alpha-bêta, proof-number search, approche hybride
  SEUIL_ORACLE.md   le cœur du sujet : choisir et valider le seuil
  PLAN.md           feuille de route, livrables, risques, questions ouvertes
  RESSOURCES.md     liens, outils, dépôts, articles (avec niveau de vérification)
```

## État de l'art en quelques chiffres

| Fait | Valeur |
|---|---|
| Positions à 8 pièces | ≈ 3,8 × 10¹⁶ |
| Syzygy 7 pièces (DTZ) | 18,4 To (2018) |
| Lomonosov 7 pièces (DTM) | 140 To (2012), hors ligne depuis 2021 |
| Op1, 8 pièces partiel (Lichess, 2025) | 63 TiB, ≈ 1,3 % des positions à 8 pièces |
| Échelle des scores Stockfish récents | +1,00 ≈ 50 % de probabilité de gain (pas une valeur de matériel) |

Détails et sources dans [`docs/ETAT_DE_L_ART.md`](docs/ETAT_DE_L_ART.md).

## Limites connues de la base de code

- Le cache du solveur ignore l'historique (règle des 50 coups, répétitions).
- Pas d'ordre des coups, pas de parallélisme : suffisant pour valider l'idée sur 4 à 6 pièces, pas pour passer à l'échelle.
- Un verdict « décisif » issu de l'oracle est une heuristique, pas une preuve : c'est précisément ce que la calibration mesure.

## Licence

MIT, voir [`LICENSE`](LICENSE).
