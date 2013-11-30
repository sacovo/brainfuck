__author__ = 'sandro'
import sys
import traceback
cells = [0]
pointer = 0
read_mode = 'a'
write_mode = 'A'
stack = []
stack_pos = 0
loop_stack = []
char_reader = None
consume_chars = ()
counter = 0
print_end = ''


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
    cells[pointer] = base_changer_in[read_mode](input())


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


def consume(c):
    global counter
    if c == consume_chars[0]:
        counter += 1
    if c == consume_chars[1]:
        counter -= 1


def loop_start():
    global consume_chars, counter
    if cells[pointer]:
        loop_stack.append(stack_pos)
    else:
        consume_chars = ('[', ']')
        counter = 1


def loop_end():
    global stack_pos
    if cells[pointer]:
        stack_pos = loop_stack[-1]
        while stack_pos < len(stack):
            process_command(stack[stack_pos])
    else:
        loop_stack.pop()


def comment():
    global counter, consume_chars
    consume_chars = ('{', '}')
    counter = 1


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

    '[': loop_start,
    ']': loop_end,

    '{': comment,

    'a': input_mode('a'),
    'b': input_mode('b'),
    'd': input_mode('d'),
    'h': input_mode('h'),

    'A': output_mode('A'),
    'B': output_mode('B'),
    'D': output_mode('D'),
    'H': output_mode('H'),
    'E': sys.exit,
}


def process_command(c):
    global stack_pos
    stack_pos += 1
    if c in function_map:
        function_map[c]()


def read(c, exclude_from_stack=False):
    if not exclude_from_stack:
        stack.append(c)
    if counter:
        consume(c)
    elif c in function_map:
        process_command(c)