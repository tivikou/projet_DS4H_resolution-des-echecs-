import chess

from echecs_solver.solver import Solver

VALUES = {chess.PAWN: 100, chess.KNIGHT: 300, chess.BISHOP: 300, chess.ROOK: 500, chess.QUEEN: 900}
MATE_IN_1 = "7k/5K2/Q7/8/8/8/8/8 w - - 0 1"  # 1.Dh6#
KQ_VS_K = "4k3/8/8/8/8/8/8/Q3K3 w - - 0 1"


class MaterialOracle:  # remplace Stockfish : matériel seul, vue des Blancs
    def cp(self, board):
        return sum(v * (len(board.pieces(p, chess.WHITE)) - len(board.pieces(p, chess.BLACK))) for p, v in VALUES.items())


def test_mat_en_un_demande_profondeur_1():
    solver = Solver(MaterialOracle(), threshold=10**6)  # seuil inatteignable : l'oracle ne décide jamais
    board = chess.Board(MATE_IN_1)
    assert solver.white_wins(board, 1)
    assert not solver.white_wins(board, 0)
    assert board.fen() == MATE_IN_1  # plateau restitué


def test_seuil_oracle():
    board = chess.Board(KQ_VS_K)  # score matériel : +900
    assert Solver(MaterialOracle(), threshold=900).white_wins(board, 0)
    assert not Solver(MaterialOracle(), threshold=901).white_wins(board, 0)


def test_nulle_par_materiel_insuffisant():
    assert not Solver(MaterialOracle(), threshold=0).white_wins(chess.Board("4k3/8/8/8/8/8/8/4K3 w - - 0 1"), 3)


def test_black_wins_est_le_miroir():
    mirrored = chess.Board(MATE_IN_1).mirror()  # trait aux Noirs, dame noire
    assert Solver(MaterialOracle(), threshold=10**6).black_wins(mirrored, 1)
