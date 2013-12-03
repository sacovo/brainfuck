__author__ = 'sandro'
import sys

# Status at beginning of runtime:
# The memory has one entry, the pointer points at the first entry
# read and write modes are both set to ascii, so input and output
# will be in letters
cells = [0]
pointer = 0
read_mode = 'a'
write_mode = 'A'
# Counter will be used for consuming the stuff between brackets
counter = 0
# Loops is used for saving the code in loops, the most inner
# loop will be stored at the rightmost place
loops = []
orig_read = None
# This is used for executing a brainfuck file
print_end = ''
# Variable implementation
variables = {}
variable_name = ''
"""
Usage:  =var=, stores the current pointer value in the variable var
        !var!, Write the value at the pointer 'var' into the current cell
        :var:, set the current pointer to the pointer of var
What is needed?
    - A method which reads the name of a variable
    - 3 methods that do the commands
    - A dict that stores the variable values
    - Some helper methods
"""


def read_var_name(c):
    """"
    Read characters from the input until a non al-num char is read, then return the name that inputted
    """
    global variable_name, read
    if c.isalnum():
        variable_name += c
    else:
        read = orig_read
        process_command(c)


def _handle_var(func):
    global read, orig_read, variable_name
    if variable_name:
        func()
        variable_name = ''
    else:
        orig_read = read
        read = read_var_name


def add_var():
    """
    If a variable name was already given, create a new variable with this name and the current pointer.
    Otherwise start to read a variable name.
    """
    global read, orig_read, variable_name
    _handle_var(lambda: variables.update({variable_name: pointer}))


def input_var():
    """
    Inputs the value of the cell at the variable position into the current cell.
    """
    def handler():
        cells[pointer] = cells[variables[variable_name]]
    _handle_var(handler)


def jump_to_var():
    """
    """
    def handler():
        global pointer
        pointer = variables[variable_name]
    _handle_var(handler)


def increment_pointer():
    """
    Increment the pointer by one (i.e. move one to the right).
    Also adjust the size of the memory array, if necessary
    """
    global pointer

    pointer += 1

    if pointer >= len(cells):
        cells.append(0)


def decrement_pointer():
    """
    Decrement the pointer by one (i.e. move on to the left).
    If already in the leftmost cell, do nothing.
    """
    global pointer
    pointer = max(0, pointer - 1)


def increment():
    """
    Increment the value at the current pointer position by one.
    """
    cells[pointer] += 1


def decrement():
    """
    Decrement the value at the current pointer position by one.
    """
    cells[pointer] -= 1


def output():
    """
    Output the the value at the current pointer position.
    The value will be formatted, according to the output_mode:
        - If output_mode is ascii (A), the value will converted to an ascii-char 65 -> 'A'
        - If output_mode is binary (B), the value will be converted to an binary number 65 -> '1000001'
        - If output_mode is decimal, the value will be outputted as decimal int 65 -> '65'
        - If output_mode is hexadecimal the value will be outputted as hexadecimal int 65 -> '41'
    If run with file, nothing else will be printed out,
    otherwise a line break will be printed out.
    @see input_()
    """
    print(base_changer_out[write_mode](cells[pointer]), end=print_end)


def input_():
    """
    Read one character from the input and save it to the current pointer position.
    The value will be converted, according to input_mode, similar to the conversion of #output.
    @attention Python is line buffered, so the user has to hit enter, in order to input something.
    @see output()
    """
    i = input() or '\n'
    cells[pointer] = base_changer_in[read_mode](i)


def input_mode(m):
    """
    Change the input mode, i.e. the mode with which the inputted chars will be converted,
    in order to store them to the memory.
    @param m: a, for ascii; b, for binary; d, for decimal and h, for hexadecimal
    """
    def mode_m():
        global read_mode
        read_mode = m

    return mode_m


def output_mode(m):
    """
    Change the way, how outputted values are converted.
    @param m: A, for ascii; B, for binary, D, for decimal and H, for hexadecimal
    """
    def mode_m():
        global write_mode
        write_mode = m
    return mode_m


def store_loop(c):
    """
    Inner method, to read the input commands and store them to loops.
    Counts the opening and closing brackets, in order to know, when it has to stop.
    @param c: character, that represents a command
    """
    global read, counter, orig_read
    if c == '[':
        counter += 1
    if c == ']':
        counter -= 1
    if counter:
        loops[-1] += c
    else:
        read = orig_read
        process_command(c)


def open_bracket():
    """
    Handle an opening bracket ('['), which indicates the beginning of a loop.
    It replaces the read method, to capture all commands after an opening bracket.
    It stores them as str into loops, as soon the read input has reached the closing bracket,
    it will replace the read method again and call <code>process_command(c)</code> with
    the closing bracket.
    """
    global counter, orig_read, read

    orig_read = read
    counter = 1
    loops.append('')

    read = store_loop


def close_bracket():
    """
    Handle a closing bracket (']').
    Get the last loop in loops and repeat its commands, until the value at the pointer position is not 0.
    """
    loop = loops.pop()
    while cells[pointer]:
        [read(c) for c in loop]


def eat(c):
    """
    Consume all input until a '}' is read, then replace the read method with the old one.
    """
    global read
    if c == '}':
        read = orig_read


def comment():
    """
    Handle a comment, starting with '{'. Replace the read method until a closing bracket ('}'), is found.
    """
    global read, orig_read
    orig_read = read
    read = eat


def clear():
    """
    Clear the memory and reset the pointer to 0. Executed when a 'c' is found.
    """
    global cells, pointer
    cells = [0]
    pointer = 0


def zero():
    """
    Reset the pointer to the first entry in the memory. Executed when a '0' is found.
    """
    global pointer
    pointer = 0


def add_empty():
    """
    Add an empty cell at the end of the memory and point the pointer at it.
    """
    global pointer
    cells.append(0)
    pointer = len(cells) - 1


def insert():
    """
    Insert a new cell at the current position and move all following cells one to the right.
    Executed when an '*' is found.
    """
    cells.insert(0, pointer)


def remove():
    """
    Remove the cell at the current position and move all the following cells one to the left.
    Executed when an 'r' is found.
    """
    del cells[pointer]

# Methods for converting the input, mapped to the lower case characters
base_changer_in = {
    'a': lambda c: ord(c[0]),
    'b': lambda c: int(c, 2),
    'd': lambda c: int(c, 10),
    'h': lambda c: int(c, 16),
}

# Methods for converting the output, mapped to the UPPER case characters
base_changer_out = {
    'A': lambda i: chr(i % 256),
    'B': lambda i: bin(i)[2:],
    'D': lambda i: i,
    'H': lambda i: hex(i)[2:],
}

# All commands, mapped with their function
function_map = {
    # Basic brainfuck commands
    '>': increment_pointer,
    '<': decrement_pointer,
    '+': increment,
    '-': decrement,
    '.': output,
    ',': input_,
    '[': open_bracket,
    ']': close_bracket,
    # Additional commands
    '{': comment,
    # change input mode
    'a': input_mode('a'),
    'b': input_mode('b'),
    'd': input_mode('d'),
    'h': input_mode('h'),
    # change output mode
    'A': output_mode('A'),
    'B': output_mode('B'),
    'D': output_mode('D'),
    'H': output_mode('H'),
    # commands handling the variables
    '=': add_var,
    '!': input_var,
    ':': jump_to_var,
    # commands handling the memory
    'c': clear,
    '0': zero,
    '*': add_empty,
    'i': insert,
    'r': remove,
    # other commands
    'E': sys.exit,
}


def process_command(c):
    """
    Process the given command, according to the function_map.
    @param c: the command to be executed
    """
    if c in function_map:
        function_map[c]()


def read(c):
    """
    Handle a command. This is a wrapper for process_command, so that the loop and comment functions work properly.
    @param c: the command to be executed
    """
    process_command(c)