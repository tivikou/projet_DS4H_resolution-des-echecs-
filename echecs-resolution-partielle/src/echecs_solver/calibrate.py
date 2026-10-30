"""Calibre le seuil de l'oracle : pour chaque seuil T, compare « |cp| >= T » à la vérité Syzygy (WDL = ±2).

Usage : python -m echecs_solver.calibrate --tb data/syzygy --material KQRvKR -n 300
"""
import argparse
import random

import chess
import chess.syzygy

from .oracle import Oracle


def random_board(material: str, rng: random.Random) -> chess.Board:
    white, black = material.split("v")  # ex. "KQRvKR"
    symbols = list(white.upper()) + list(black.lower())
    while True:
        board = chess.Board(None)
        for sq, s in zip(rng.sample(range(64), len(symbols)), symbols):
            board.set_piece_at(sq, chess.Piece.from_symbol(s))
        board.turn = rng.random() < 0.5
        if board.is_valid() and not board.is_game_over():  # écarte pions en 1re/8e rangée, rois adjacents, etc.
            return board


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tb", required=True, help="dossier des tables Syzygy (WDL)")
    ap.add_argument("--material", default="KQvK", help="un roi de chaque côté, ex. KQRvKR")
    ap.add_argument("-n", type=int, default=200, help="nombre de positions")
    ap.add_argument("--depth", type=int, default=14, help="profondeur Stockfish")
    ap.add_argument("--stockfish", default="stockfish")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--thresholds", type=int, nargs="+", default=[100, 300, 500, 900, 1500, 3000])
    a = ap.parse_args()

    rng = random.Random(a.seed)
    rows, misses = [], 0  # (cp, wdl) du point de vue des Blancs
    with Oracle(a.stockfish, a.depth) as oracle, chess.syzygy.open_tablebase(a.tb, load_dtz=False) as tb:
        while len(rows) < a.n:
            board = random_board(a.material, rng)
            wdl = tb.get_wdl(board)
            if wdl is None:
                misses += 1
                if misses > 100 and not rows:
                    raise SystemExit(f"Tables Syzygy introuvables pour {a.material} dans {a.tb}")
                continue
            rows.append((oracle.cp(board), wdl if board.turn else -wdl))

    truth = sum(abs(w) == 2 for _, w in rows)
    print(f"{a.material} : {len(rows)} positions, {truth} gagnantes (Stockfish depth {a.depth}, seed {a.seed})")
    print("seuil_cp  décisifs  faux_décisifs  précision  rappel")
    for t in a.thresholds:
        pred = sum(abs(cp) >= t for cp, _ in rows)
        tp = sum((cp >= t and w == 2) or (cp <= -t and w == -2) for cp, w in rows)
        prec = tp / pred if pred else float("nan")
        rec = tp / truth if truth else float("nan")
        print(f"{t:8d} {pred:9d} {pred - tp:14d} {prec:10.3f} {rec:7.3f}")


if __name__ == "__main__":
    main()
