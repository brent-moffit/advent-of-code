from io import TextIOWrapper
from pathlib import Path
from typing import Callable

from d2.strategy_decoders import GameRound, outcome_decoder, player_throw_decoder

StrategyDecoder = Callable[[str], GameRound]


class StrategyGuide:
    def __init__(self, file_path: str | Path, decoder: StrategyDecoder) -> None:
        file_path = Path(file_path).resolve()
        self.decode_strategy = decoder

        with open(file_path) as file:
            self.score = self._simulate(file)

    def _simulate(self, file: TextIOWrapper) -> int:
        score = 0

        while line := file.readline():
            round = self.decode_strategy(line)
            score += round.player_score

        return score


if __name__ == "__main__":
    print("--- Part One ---")
    print("Simulating game with player throw strategy")
    game = StrategyGuide("input.txt", decoder=player_throw_decoder)
    print(f"Simulated Score: {game.score}")
    print()

    print("--- Part Two ---")
    print("Simulating game with outcome strategy")
    game = StrategyGuide("input.txt", decoder=outcome_decoder)
    print(f"Simulated Score: {game.score}")
    print()
