"""Preuve bornée « les Blancs gagnent » : arbre ET/OU dont les feuilles sont
une table de finales (verdict exact) ou l'oracle (verdict heuristique, seuil en centipions)."""
import chess
import chess.polyglot


class Solver:
    def __init__(self, oracle, tb=None, threshold: int = 900, tb_max_pieces: int = 7):
        self.oracle, self.tb = oracle, tb
        self.threshold, self.tb_max_pieces = threshold, tb_max_pieces
        # shortcut: clé sans historique (règle des 50 coups, répétitions ignorées) ; à revoir si ça fausse des résultats
        self.cache: dict[tuple[int, int], bool] = {}

    def white_wins(self, board: chess.Board, depth: int) -> bool:
        """depth en demi-coups. Le plateau est restitué intact."""
        if board.is_checkmate():
            return board.turn == chess.BLACK
        if board.is_stalemate() or board.is_insufficient_material():
            return False
        key = (chess.polyglot.zobrist_hash(board), depth)
        if key not in self.cache:
            self.cache[key] = self._solve(board, depth)
        return self.cache[key]

    def black_wins(self, board: chess.Board, depth: int) -> bool:
        return self.white_wins(board.mirror(), depth)  # même position, couleurs échangées

    def _solve(self, board: chess.Board, depth: int) -> bool:
        wdl = self._tb_wdl(board)
        if wdl is not None:  # exact ; une victoire « cursed » (nulle aux 50 coups) ne compte pas
            return wdl == 2 if board.turn == chess.WHITE else wdl == -2
        if self.oracle.cp(board) >= self.threshold:
            return True  # décisif selon l'oracle : heuristique, pas une preuve
        if depth == 0:
            return False
        results = (self._child(board, m, depth - 1) for m in list(board.legal_moves))
        return any(results) if board.turn == chess.WHITE else all(results)  # OU pour les Blancs, ET pour les Noirs

    def _tb_wdl(self, board: chess.Board):
        if self.tb is None or board.castling_rights or board.occupied.bit_count() > self.tb_max_pieces:
            return None  # Syzygy ne gère pas le roque
        return self.tb.get_wdl(board)  # None si la table est absente

    def _child(self, board: chess.Board, move: chess.Move, depth: int) -> bool:
        board.push(move)
        try:
            return self.white_wins(board, depth)
        finally:
            board.pop()
