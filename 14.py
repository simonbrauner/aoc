from collections import Counter, defaultdict


def template_after_steps(
    template: dict[str, int], rules: dict[str, str], steps: int
) -> dict[str, int]:
    before_step = template

    for _ in range(steps):
        after_step: dict[str, int] = defaultdict(int)

        for pair, quantity in before_step.items():
            after_step[pair[0] + rules[pair]] += quantity
            after_step[rules[pair] + pair[1]] += quantity

        before_step = after_step

    return before_step


def polymer_subtraction(
    template: dict[str, int], corners: str, rules: dict[str, str], steps: int
) -> int:
    after_steps = template_after_steps(template, rules, steps)
    element_quantities: dict[str, float] = defaultdict(int)

    for pair, quantity in after_steps.items():
        for element in pair:
            element_quantities[element] += quantity / 2

    for remaining in corners:
        element_quantities[remaining] += 0.5

    return int(max(element_quantities.values()) - min(element_quantities.values()))


with open("data.txt") as f:
    line = f.readline().strip()
    f.readline()
    template = Counter([line[x : x + 2] for x in range(len(line) - 1)])
    corners = line[0] + line[-1]

    rules = {}

    while (line := f.readline().strip()) != "":
        split = line.split(" -> ")
        rules[split[0]] = split[1]

    print(polymer_subtraction(template, corners, rules, 10))
    print(polymer_subtraction(template, corners, rules, 40))
