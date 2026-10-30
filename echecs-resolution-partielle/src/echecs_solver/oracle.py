"""Oracle Stockfish : score en centipions du point de vue des Blancs."""
import chess
import chess.engine

MATE = 100_000  # valeur attribuée à un mat forcé


class Oracle:
    def __init__(self, path: str = "stockfish", depth: int = 14, threads: int = 1, hash_mb: int = 128):
        self.engine = chess.engine.SimpleEngine.popen_uci(path)
        self.engine.configure({"Threads": threads, "Hash": hash_mb})
        self.limit = chess.engine.Limit(depth=depth)  # fixer aussi la version de Stockfish : l'échelle des cp change

    def cp(self, board: chess.Board) -> int:
        return self.engine.analyse(board, self.limit)["score"].white().score(mate_score=MATE)

    def close(self) -> None:
        self.engine.quit()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
