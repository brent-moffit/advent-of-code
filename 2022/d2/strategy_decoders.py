from typing import Mapping
from d2.game_round import Throw, Outcome, GameRound

PLAYER_THROW_MAPPING: Mapping[str, Throw] = {
    "X": Throw.ROCK,
    "Y": Throw.PAPER,
    "Z": Throw.SCISSORS,
}

OPPONENT_THROW_MAPPING: Mapping[str, Throw] = {
    "A": Throw.ROCK,
    "B": Throw.PAPER,
    "C": Throw.SCISSORS,
}


def player_throw_decoder(line: str) -> GameRound:
    opponent_code, player_code = line.split()
    return GameRound(
        PLAYER_THROW_MAPPING[player_code],
        OPPONENT_THROW_MAPPING[opponent_code],
    )


OUTCOME_MAPPING: Mapping[str, Outcome] = {
    "X": Outcome.LOSS,
    "Y": Outcome.DRAW,
    "Z": Outcome.WIN,
}


def outcome_decoder(line: str) -> GameRound:
    opponent_code, outcome_code = line.split()
    opponent = OPPONENT_THROW_MAPPING[opponent_code]
    outcome = OUTCOME_MAPPING[outcome_code]

    match outcome:
        case Outcome.WIN:
            player = Throw.wins_against(opponent)
        case Outcome.DRAW:
            player = opponent
        case Outcome.LOSS:
            player = Throw.loses_against(opponent)

    return GameRound(player, opponent)
