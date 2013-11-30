import fileinput

__author__ = 'sandro'
import getopt
import sys
from brainfuck import interpreter


def main():
    opts, args = getopt.getopt(sys.argv[1:], "f")
    for opt, arg in opts:
        if 'f' in opt:
            for line in fileinput.input(sys.argv[2:]):
                for c in line:
                    interpreter.read(c)
            sys.exit()
    interpreter.print_end = '\n'
    while True:
        for line in input('>>> '):
            for c in line:
                interpreter.read(c)