from dataclasses import dataclass, field
from io import TextIOWrapper
from itertools import count
from operator import attrgetter
from pathlib import Path
from typing import ClassVar, Iterator


@dataclass
class Carrier:
    _id_counter: ClassVar[Iterator[int]] = count()

    id: int = field(init=False, default_factory=lambda: next(Carrier._id_counter))
    inventory: list[int] = field(default_factory=list)

    @property
    def totalInventory(self) -> int:
        return sum(self.inventory)

    def __str__(self) -> str:
        return f"🧝 Elf {self.id}"


class InventoryParser:
    def __init__(self, input_path: str | Path) -> None:
        input_path = Path(input_path).resolve()

        with open(input_path) as file:
            self.carriers = self._parse_carriers(file)

    @staticmethod
    def _parse_carriers(file: TextIOWrapper) -> list[Carrier]:
        result: list[Carrier] = []
        current_carrier = Carrier()

        while line := file.readline():
            match line.split():
                case [str(item)] if item.isdigit():
                    current_carrier.inventory.append(int(item))
                case []:
                    result.append(current_carrier)
                    current_carrier = Carrier()
                case _:
                    raise RuntimeError(f"Unexpected input: {line}")

        result.append(current_carrier)

        return result


if __name__ == "__main__":
    elves = InventoryParser("input.txt")

    print("--- Part One ---")
    snack_elf = max(elves.carriers, key=attrgetter("totalInventory"))
    print(f"Elf carrying the most calories: {snack_elf}")
    print(f"Calories carried {snack_elf.totalInventory}")
    print()

    print("--- Part Two ---")
    elves.carriers.sort(key=attrgetter("totalInventory"), reverse=True)
    top_elves = elves.carriers[:3]
    top_calories = sum(e.totalInventory for e in top_elves)
    print("Elves carrying the most calories:")
    print(*top_elves, sep=", ")
    print(f"Total calories they carry: {top_calories}")
    print()
