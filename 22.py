from __future__ import annotations
from math import prod
from dataclasses import dataclass
from collections.abc import Callable
from collections import defaultdict


@dataclass
class Cuboid:
    on: bool
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int

    def __hash__(self) -> int:
        return hash(
            (self.min_x, self.max_x, self.min_y, self.max_y, self.min_z, self.max_z)
        )

    def cube_count(self) -> int:
        return prod(
            [
                self.max_x - self.min_x + 1,
                self.max_y - self.min_y + 1,
                self.max_z - self.min_z + 1,
            ]
        )

    def overlaps(self, other: Cuboid) -> bool:
        return (
            points_overlap(self.min_x, self.max_x, other.min_x, other.max_x)
            or points_overlap(self.min_y, self.max_y, other.min_y, other.max_y)
            or points_overlap(self.min_z, self.max_z, other.min_z, other.max_z)
        )


def read_range(line: str, coordinate: str) -> tuple[int, int]:
    split = line.split(f"{coordinate}=")[1].split(",")[0]
    left, right = split.split("..")

    return int(left), int(right)


def points_overlap(
    first_min: int, first_max: int, second_min: int, second_max: int
) -> bool:
    return (
        first_min <= second_min <= first_max
        or first_min <= second_max <= first_max
        or second_min <= first_min <= second_max
        or second_min <= first_max <= second_max
    )


def in_initialization_procedure(step: Cuboid) -> bool:
    return all(
        [
            abs(x) <= 50
            for x in [
                step.min_x,
                step.max_x,
                step.min_y,
                step.max_y,
                step.min_z,
                step.max_z,
            ]
        ]
    )


def cubes_on_count(
    steps: list[Cuboid], step_filter: None | Callable[[Cuboid], bool] = None
) -> int:
    on: set[Cuboid] = set()
    off: set[Cuboid] = set()

    for step in filter(step_filter, steps):
        if step.on:
            on.add(step)
        else:
            off.add(step)

    return sum([x.cube_count() for x in on]) - sum([x.cube_count() for x in off])


with open("data.txt") as f:
    steps = []

    for line in f:
        line = line.replace("\n", ",")
        x = read_range(line, "x")
        y = read_range(line, "y")
        z = read_range(line, "z")
        steps.append(
            Cuboid(line.split(" ")[0] == "on", x[0], x[1], y[0], y[1], z[0], z[1])
        )

    print(cubes_on_count(steps, in_initialization_procedure))
