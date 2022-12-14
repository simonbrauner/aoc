from collections.abc import Callable


HIGHEST_TO_LOWEST = range(9, 0, -1)
LOWEST_TO_HIGHEST = range(1, 10)

FUNCTIONS: dict[str, Callable[[int, int], int]] = {
    "add": lambda x, y: x + y,
    "mul": lambda x, y: x * y,
    "div": lambda x, y: int(x / y),
    "mod": lambda x, y: x % y,
    "eql": lambda x, y: 1 if x == y else 0,
}


class Instruction:
    def __init__(self, raw: str):
        split = raw.split()
        self.name = split[0]
        self.variable = split[1]
        self.value = split[2]

    def __repr__(self) -> str:
        return f"{self.name} {self.variable} {self.value}"

    def evaluate(self, variables: dict[str, int]) -> None:
        value = variables[self.value] if self.value in variables else int(self.value)

        variables[self.variable] = FUNCTIONS[self.name](variables[self.variable], value)


def run_program_part(
    program: list[list[Instruction]],
    z: int,
    inputs: list[int],
    cache: set[tuple[int, int, int]],
    digit_order: range,
) -> bool:
    if len(program) == len(inputs):
        return z == 0

    for digit in digit_order:
        cache_item = digit, len(inputs), z
        if cache_item in cache:
            return False

        variables = {"w": digit, "x": 0, "y": 0, "z": z}
        inputs.append(digit)

        for instruction in program[len(inputs) - 1]:
            instruction.evaluate(variables)

        if run_program_part(program, variables["z"], inputs, cache, digit_order):
            return True

        cache.add(cache_item)
        inputs.pop()

    return False


def print_edge_model_numbers(program: list[list[Instruction]]) -> None:
    cache: set[tuple[int, int, int]] = set()

    for digit_range in HIGHEST_TO_LOWEST, LOWEST_TO_HIGHEST:
        inputs: list[int] = []
        run_program_part(program, 0, inputs, cache, digit_range)
        print(int("".join([str(x) for x in inputs])))


with open("data.txt") as f:
    program = []
    part: list[Instruction] = []

    assert f.readline().strip() == "inp w"

    while (line := f.readline().strip()) != "":
        if line == "inp w":
            program.append(part)
            part = []
        else:
            part.append(Instruction(line))
    program.append(part)

    print_edge_model_numbers(program)
