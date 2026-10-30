# Feuille de route

Tailles relatives : **S** (une séance), **M** (quelques séances), **L** (plusieurs semaines).

## Phase 0 : mise en place (S)

- [ ] Installer Python ≥ 3.10, le dépôt (`pip install -e ".[dev]"`), lancer `pytest`.
- [ ] Installer Stockfish ; noter la version exacte (`uci` renvoie le nom et la version).
- [ ] Télécharger les tables Syzygy 3-4-5 pièces (≈ 1 Go), vérifier les sommes de contrôle.
- [ ] Créer le dépôt GitHub, activer la CI (`.github/workflows/ci.yml`).

## Phase 1 : calibrer le seuil (M) — cœur du sujet

- [ ] Lancer `calibrate.py` sur KQvK, KRvK, KQvKR, KRPvKR, KQRvKR (graine fixée, ≥ 1000 positions).
- [ ] Tracer précision et rappel selon T, pour plusieurs profondeurs.
- [ ] Lister et étudier à la main les faux décisifs (catégories de `SEUIL_ORACLE.md`).
- [ ] Comparer score absolu, probabilité de gain WDL, critère matériel.
- [ ] Livrable : tableau « seuil minimal pour une précision ≥ 99 % / 99,9 % » par famille.

## Phase 2 : solveur borné validé (M)

- [ ] Compter séparément les feuilles table / oracle / profondeur épuisée dans le résultat.
- [ ] Ordre des coups (captures, échecs, promotions d'abord).
- [ ] Valider : sur ≤ 6 pièces, sans oracle, le solveur doit retrouver les verdicts Syzygy.
- [ ] Mesurer : nœuds visités et appels d'oracle avec et sans seuil.
- [ ] Livrable : courbe « coût de la preuve selon T ».

## Phase 3 : passer à l'échelle (L)

- [ ] Cache persistant (SQLite ou LMDB), clés canonicalisées par symétrie.
- [ ] Parallélisme (un Stockfish par cœur).
- [ ] Proof-number search ou df-pn à la place du minimax borné.
- [ ] Sonder 6 pièces en local ; 7 pièces via l'API Lichess ⚠ ou des tables locales si l'espace disque le permet.
- [ ] Premier essai « avec une dame d'avance » à 8–10 pièces : verdicts conditionnels, sans vérité terrain.

## Phase 4 : validation pratique (M)

- [ ] Parties Stockfish limité (« joueur occasionnel ») contre Stockfish complet, depuis des positions de score donné.
- [ ] Relier le seuil T à un score de match.

## Phase 5 : rédaction (M)

Plan de rapport : introduction ; état de l'art ; méthode (solveur, oracle, calibration) ; expériences ; résultats ; limites ; perspectives.

## Reproductibilité (à noter pour chaque expérience)

Version de Stockfish, profondeur ou nombre de nœuds, `Threads` et `Hash`, graine, matériel testé, nombre de positions, version de python-chess, date et commit du dépôt. Sauvegarder les résultats bruts (JSONL ou CSV) dans `results/` (ignoré par git, à archiver ailleurs).

## Risques

| Risque | Parade |
|---|---|
| Stockfish non déterministe (threads, temps) | profondeur fixe, `Threads=1` pour la calibration |
| Échelle de score qui change entre versions | version figée et notée |
| Échantillon aléatoire peu réaliste | deuxième jeu de positions issues de parties |
| Explosion combinatoire | commencer à 4–5 pièces, profondeur bornée, cache |
| Tables volumineuses | 3-4-5 pièces (≈ 1 Go) suffisent pour démarrer ; 6 pièces en option |
| Faux sentiment de preuve | séparer verdicts exacts et verdicts d'oracle dans tous les résultats |

## Questions ouvertes

1. Le seuil dépend-il du nombre de pièces ou du type de matériel ?
2. Quelle part des positions « décisives » selon l'oracle sont de vrais gains à 6–7 pièces ?
3. Peut-on estimer l'erreur à 8 pièces avec Op1 comme vérité partielle ?
4. Un seuil en probabilité de gain est-il plus stable qu'un seuil en centipions entre versions de Stockfish ?
5. Que signifie « battre un grand joueur » : quel niveau, quel contrôle de temps ?
