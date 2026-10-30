# Ressources

Légende : ✅ consulté pendant la création du dépôt ; ⚠ cité de mémoire ou vu seulement dans des résultats de recherche : vérifier le lien avant de le citer.

## Tables de finales

| Ressource | Lien | |
|---|---|---|
| Blog Lichess : Op1, table partielle à 8 pièces | https://lichess.org/@/Lichess/blog/op1-partial-8-piece-tablebase-available/1ptPBDpC | ✅ |
| Wikipédia : Endgame tablebase | https://en.wikipedia.org/wiki/Endgame_tablebase | ✅ |
| Documentation python-chess : sondage Syzygy | https://python-chess.readthedocs.io/en/latest/syzygy.html | ✅ |
| ChessBase : premiers résultats et entretien sur les 8 pièces | https://en.chessbase.com/newsroom/post/8-piece-endgame-tablebases-first-findings-and-interview | ⚠ |
| TalkChess : « How is work on 8-man tablebases progressing? » | https://talkchess.com/viewtopic.php?p=969195 | ⚠ |
| Chess Programming Wiki (Syzygy Bases, Endgame Tablebases) | https://www.chessprogramming.org | ⚠ |
| Générateur Syzygy (Ronald de Man) | https://github.com/syzygy1/tb | ⚠ |
| Fathom : bibliothèque autonome de sondage Syzygy | https://github.com/jdart1/Fathom | ⚠ |
| Serveur tablebase de Lichess | https://github.com/lichess-org/lila-tablebase | ⚠ |
| API Lichess : `https://tablebase.lichess.ovh/standard?fen=<FEN>` (à utiliser avec modération) | https://tablebase.lichess.ovh | ⚠ |
| Miroirs de téléchargement Syzygy 3-4-5, 6 et 7 pièces | à chercher depuis la documentation de Lichess ou de Stockfish | ⚠ |

Téléchargement des tables : vérifier la taille avant de lancer (3-4-5 pièces ≈ 1 Go ; 6 pièces ≈ 160 Go en DTZ ; 7 pièces ≈ 18,4 To en DTZ ✅) et les sommes de contrôle fournies avec les fichiers.

## Stockfish et évaluation

| Ressource | Lien | |
|---|---|---|
| Dépôt `WDL_model` (conversion score → probabilité de gain) | https://github.com/official-stockfish/WDL_model | ✅ |
| Variante `vondele/wdl_model` | https://github.com/vondele/wdl_model | ⚠ |
| Article « Stockfish Normalizes Its Evaluation » | https://thechessmind.substack.com/p/news-you-can-use-stockfish-normalizes | ⚠ |
| Téléchargement de Stockfish | https://stockfishchess.org/download/ | ⚠ |
| Dépôt Stockfish | https://github.com/official-stockfish/Stockfish | ⚠ |

Options UCI utiles : `Threads`, `Hash`, `SyzygyPath`, `UCI_ShowWDL` ✅, `UCI_LimitStrength` et `UCI_Elo` ⚠, `MultiPV`.

## Bibliothèques

| Ressource | Rôle |
|---|---|
| python-chess (`pip install chess`, import `chess`) | plateau, UCI, sondage Syzygy ✅ |
| Fathom (C) | sonder Syzygy hors Python ⚠ |

Les versions de dépendances sont à fixer dans `pyproject.toml` ; ce dépôt demande `chess>=1.11` (la documentation consultée correspond à python-chess 1.11.2 ✅).

## Lectures théoriques ⚠ (de mémoire, à retrouver)

- Victor Allis, *Searching for Solutions in Games and Artificial Intelligence* (thèse, 1994) : niveaux de résolution, proof-number search.
- Jonathan Schaeffer et al., *Checkers Is Solved*, Science, 2007.
- Claude Shannon, *Programming a Computer for Playing Chess*, 1950 : nombre de Shannon, première analyse de la complexité.
- Ken Thompson : travaux sur les finales à 5 et 6 pièces.
- Eugene Nalimov : tables de finales DTM.

## Communautés et suivi

- Forum TalkChess (section programmation) ⚠
- Discord et forum Lichess ⚠
- Blog Lichess : annonces des tables de finales ✅ (Op1)
