from dataclasses import dataclass
from enum import StrEnum, auto
from typing import ClassVar, Mapping


class Throw(StrEnum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()

    @classmethod
    def wins_against(cls, throw: "Throw") -> "Throw":
        match throw:
            case Throw.ROCK:
                return Throw.PAPER
            case Throw.PAPER:
                return Throw.SCISSORS
            case Throw.SCISSORS:
                return Throw.ROCK

    @classmethod
    def loses_against(cls, throw: "Throw") -> "Throw":
        match throw:
            case Throw.ROCK:
                return Throw.SCISSORS
            case Throw.PAPER:
                return Throw.ROCK
            case Throw.SCISSORS:
                return Throw.PAPER


class Outcome(StrEnum):
    WIN = auto()
    DRAW = auto()
    LOSS = auto()


@dataclass
class GameRound:
    THROW_SCORE: ClassVar[Mapping[Throw, int]] = {
        Throw.ROCK: 1,
        Throw.PAPER: 2,
        Throw.SCISSORS: 3,
    }

    player_throw: Throw
    opponent_throw: Throw

    @property
    def outcome(self) -> Outcome:
        result = None

        match self.player_throw, self.opponent_throw:
            case p, o if p == Throw.wins_against(o):
                result = Outcome.WIN
            case p, o if p == o:
                result = Outcome.DRAW
            case p, o if p == Throw.loses_against(o):
                result = Outcome.LOSS

        if not result:
            raise RuntimeError(
                "Unable to determine for round: "
                f"{self.player_throw=}, {self.opponent_throw=}"
            )

        return result

    @property
    def player_score(self) -> int:
        score = GameRound.THROW_SCORE[self.player_throw]

        match self.outcome:
            case Outcome.WIN:
                score += 6
            case Outcome.DRAW:
                score += 3

        return score
