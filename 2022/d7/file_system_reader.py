from collections.abc import Iterator
from dataclasses import dataclass, field
from functools import cached_property
from io import TextIOWrapper
from operator import attrgetter
from pathlib import Path
from typing import Protocol


class FileLike(Protocol):
    @property
    def name(self) -> str:
        ...

    @property
    def size(self) -> int:
        ...

    def __str__(self, level: int = 0) -> str:
        ...


@dataclass
class File:
    name: str
    size: int

    def __str__(self, level: int = 0) -> str:
        return "  " * level + f"📄 {self.name} (file, {self.size=})"


class Directory:
    def __init__(self, name) -> None:
        self.name = name
        self._children: dict[str, FileLike] = {}

    @property
    def children(self) -> dict[str, FileLike]:
        self._clear_size_cache()
        return self._children

    @children.setter  # type: ignore [attr-defined]
    def set_children(self, value: dict[str, FileLike]):
        self._clear_size_cache()
        self._children = value

    @children.deleter  # type: ignore [attr-defined]
    def del_children(self) -> None:
        self._clear_size_cache()
        del self._children
        self._children = {}

    @cached_property
    def size(self):
        return sum(c.size for c in self.children.values())

    def files(self) -> Iterator[File]:
        return (f for f in self._children.values() if isinstance(f, File))

    def subdirectories(self) -> Iterator["Directory"]:
        return (d for d in self._children.values() if isinstance(d, Directory))

    def __str__(self, level: int = 0) -> str:
        padding = "  " * level
        header = [padding + f"📁 {self.name} (dir, {self.size=})"]
        body = [c.__str__(level + 1) for c in self._children.values()]
        return "\n".join(header + body)

    def _clear_size_cache(self):
        try:
            del self.size
        except AttributeError:
            pass


class FileSystemReader:
    def __init__(self, input_file: str | Path) -> None:
        self.root = Directory("/")
        self.input_path = Path(input_file).resolve()

        if not self.input_path.exists() or not self.input_path.is_file():
            raise FileNotFoundError("Input file does not exist")

        self.scan()

    def all_directories(self) -> Iterator[Directory]:
        dirs = [self.root]

        while dirs:
            current_dir = dirs.pop()
            dirs.extend(current_dir.subdirectories())

            yield current_dir

    def scan(self):
        current_path = [self.root]

        with open(self.input_path) as input_file:
            while command := input_file.readline():
                match command.split():
                    case ["$", "cd", "/"]:
                        current_path = [self.root]
                    case ["$", "cd", ".."]:
                        current_path.pop()
                    case ["$", "cd", dir] if dir in current_path[-1].subdirectories():
                        current_path.append(current_path[-1].children[dir])
                    case ["$", "cd", dir]:
                        next_dir = Directory(dir)
                        current_path[-1].children[dir] = next_dir
                        current_path.append(next_dir)
                    case ["$", "ls"]:
                        files = self.read_ls_output(input_file)
                        current_path[-1].children.update(
                            {file.name: file for file in files}
                        )
                    case ["$", unknown, *_]:
                        raise RuntimeError(f"Unknown command {unknown}: {command}")
                    case _:
                        raise RuntimeError(f"Expected command: {command}")

    @staticmethod
    def read_ls_output(
        input_file: TextIOWrapper, *, include_directories: bool = False
    ) -> list[FileLike]:
        result: list[FileLike] = []
        seek_position = input_file.tell()

        while line := input_file.readline():
            match line.split():
                case ["$", *_]:
                    input_file.seek(seek_position)
                    break
                case ["dir", str(name)]:
                    if include_directories:
                        result.append(Directory(name))
                case [str(size), str(name)] if size.isdigit():
                    result.append(File(name, int(size)))
                case _:
                    raise RuntimeError(f"Unexpected output to ls command: {line}")

            seek_position = input_file.tell()

        return result


if __name__ == "__main__":
    file_system = FileSystemReader("input.txt")

    print("File System:")
    print(file_system.root)
    print()

    print("--- Part One ---")
    print("Total size of all directories smaller than 100000:", end=" ")
    print(sum(d.size for d in file_system.all_directories() if d.size <= 100000))
    print()

    print("--- Part Two ---")
    total_disk = 70_000_000
    update_size = 30_000_000
    used_disk = file_system.root.size
    unused_disk = total_disk - used_disk
    space_needed = update_size - unused_disk
    target_dir = min(
        (d for d in file_system.all_directories() if d.size >= space_needed),
        key=attrgetter("size"),
    )

    print(f"Smallest directory that will free up {space_needed}: {target_dir.name}")
    print(f"Directory size: {target_dir.size}")
    print()
