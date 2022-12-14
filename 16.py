from collections.abc import Callable
from math import prod
from collections import deque


PACKET_LITERAL = 4
LENGTH_TYPE_NUMBER_OF_BITS = 0
LENGTH_TYPE_NUMBER_OF_PACKETS = 1
LENGTH_TYPE_COUNTS = {0: 15, 1: 11}
OPERATORS: dict[int, Callable[[list[int]], int]] = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: lambda x: 1 if x[0] > x[1] else 0,
    6: lambda x: 1 if x[0] < x[1] else 0,
    7: lambda x: 1 if x[0] == x[1] else 0,
}


def add_hex_to_bits(bits: deque[int], letter: str) -> None:
    hexadecimal = int(letter, base=16)

    for possible_divisor in [8, 4, 2, 1]:
        if hexadecimal >= possible_divisor:
            hexadecimal -= possible_divisor
            bits.append(1)
        else:
            bits.append(0)


def read_bits(bits: deque[int], count: int) -> int:
    result = 0

    for _ in range(count):
        result *= 2
        result += bits.popleft()

    return result


def read_number(bits: deque[int]) -> int:
    number_bits = deque[int]()
    last = False

    while not last:
        last = read_bits(bits, 1) == 0

        for _ in range(4):
            number_bits.append(read_bits(bits, 1))

    return read_bits(number_bits, len(number_bits))


def read_packets(bits: deque[int]) -> tuple[int, int]:
    version_sum = read_bits(bits, 3)
    packet_type = read_bits(bits, 3)

    if packet_type == PACKET_LITERAL:
        return version_sum, read_number(bits)

    operands = []
    length_type = read_bits(bits, 1)
    length = read_bits(bits, LENGTH_TYPE_COUNTS[length_type])

    if length_type == LENGTH_TYPE_NUMBER_OF_BITS:
        total_length = len(bits)

        while len(bits) > total_length - length:
            result = read_packets(bits)
            version_sum += result[0]
            operands.append(result[1])
    else:
        for _ in range(length):
            result = read_packets(bits)
            version_sum += result[0]
            operands.append(result[1])

    return version_sum, OPERATORS[packet_type](operands)


with open("data.txt") as f:
    bits = deque[int]()

    for letter in f.readline().strip():
        add_hex_to_bits(bits, letter)

    result = read_packets(bits)
    print(result[0])
    print(result[1])
