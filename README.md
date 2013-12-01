brainfuck
=========
Brainfuck interpreter, written in python.

This interpreter is written for training purposes.

It follows the brainfuck standards on http://en.wikipedia.org/wiki/Brainfuck and adds a few extra commands.
All available commands are listed here:
  - '>': Move pointer one to the right
  - '<': Move pointer one to the left
  - '+': Increase value at pointer by one
  - '-': Decrease value at pointer by one
  - '.': Output value at pointer position (for converting, see below)
  - ',': Read value from the user into value at pointer (for converting, see below)
  - '[': Start of a loop, if the value at pointer is 0, the following part will be left out, until closing ']'
  - '[': End of a loop, if value at pointer is not 0 all code since the opening '[' will be executed again
  - '{': Begining of a comment, code that follows after this will be ignored until the closing '}'
  - '}': End of a comment. **Note:** Comments can't be nested, a '}' will alway terminate the comment
  - 'a': Change the input mode to ascii, so ',' will read one character from the user and convert it to number (default)
  - 'b': Change input mode to binary, all input will be read as binary number
  - 'd': Change input mode to decimal, numbers will be read as decimal number
  - 'h': Change input mode to hexdecimal, numbers will be read as hexadecimal number
  - 'A': Change the converting for output to ascii, so all numbers will be converted to an ascii char, if the char is to big, the modulo of 256 will be used (default)
  - 'B': Change the output mode to binary
  - 'D': Change the output mode to decimal
  - 'H': Change the output mode to hexadecimal
  - 'c': Clear the memory and reset the pointer to 0
  - '0': Reset the pointer to 0 (the leftmos cell)
  - '*': Insert a cell with the value 0 at the current position and move all following cells one to the right
  - 'r': Remove the cell at the current pointer and move all following cells one to the left
  - 'E': Exit the programm
