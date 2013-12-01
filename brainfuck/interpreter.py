__author__ = 'sandro'
import sys

cells = [0]
pointer = 0
read_mode = 'a'
write_mode = 'A'
print_end = ''

counter = 0
loops = []


def increment_pointer():
    global pointer

    pointer += 1

    if pointer >= len(cells):
        cells.append(0)


def decrement_pointer():
    global pointer

    pointer -= 1


def increment():
    cells[pointer] += 1


def decrement():
    cells[pointer] -= 1


def output():
    print(base_changer_out[write_mode](cells[pointer]), end=print_end)


def input_():
    i = input() or '\n'
    cells[pointer] = base_changer_in[read_mode](i)


def input_mode(m):

    def mode_m():
        global read_mode
        read_mode = m

    return mode_m


def output_mode(m):

    def mode_m():
        global write_mode
        write_mode = m
    return mode_m


def open_bracket():
    global read, counter

    orig_read = read
    counter = 1
    loops.append('')

    def test(c):
        global read, counter, test
        if c == '[':
            counter += 1
        if c == ']':
            counter -= 1
        if counter:
            loops[-1] += c
        else:
            read = orig_read
            process_command(c)

    read = test


def close_bracket():
    loop = loops.pop()
    while cells[pointer]:
        for c in loop:
            read(c)


def comment():
    global read
    orig_read = read

    def eat(c):
        global read
        if c == '}':
            read = orig_read

    read = eat


def clear():
    global cells, pointer
    cells = [0]
    pointer = 0


def zero():
    global pointer
    pointer = 0


def add_empty():
    global pointer
    cells.append(0)
    pointer = len(cells) - 1


def insert():
    cells.insert(0, pointer)


def remove():
    del cells[pointer]

base_changer_in = {
    'a': lambda c: ord(c[0]),
    'b': lambda c: int(c, 2),
    'd': lambda c: int(c, 10),
    'h': lambda c: int(c, 16),
}

base_changer_out = {
    'A': lambda i: chr(i % 256),
    'B': lambda i: bin(i)[2:],
    'D': lambda i: i,
    'H': lambda i: hex(i)[2:],
}

function_map = {
    '>': increment_pointer,
    '<': decrement_pointer,
    '+': increment,
    '-': decrement,
    '.': output,
    ',': input_,

    '[': open_bracket,
    ']': close_bracket,

    '{': comment,

    'a': input_mode('a'),
    'b': input_mode('b'),
    'd': input_mode('d'),
    'h': input_mode('h'),

    'A': output_mode('A'),
    'B': output_mode('B'),
    'D': output_mode('D'),
    'H': output_mode('H'),

    'c': clear,
    '0': zero,
    '*': add_empty,
    'i': insert,
    'r': remove,

    'E': sys.exit,
}


def process_command(c):
    if c in function_map:
        function_map[c]()


def read(c):
    process_command(c)