#!/bin/python3
import os
import sys
from subprocess import call
import ntpath

C_FILE_HEADER = """
#include <stdio.h>
int main() {
char array[30000]={0};
char *ptr=array;
"""

C_FILE_FOOTER = "return 0;}"

C_REP_SHIFT_RIGHT = '++ptr;'
C_REP_SHIFT_LEFT = '--ptr;'
C_REP_INCREMENT = '++*ptr;'
C_REP_DECREMENT = '--*ptr;'
C_REP_PRINT = 'putchar(*ptr);'
C_REP_READ = '*ptr=getchar();'
C_REP_LOOP_START = 'while(*ptr){'
C_REP_LOOP_END = '}'

if len(sys.argv) != 2:
    print("Usage: {} <file>".format(sys.argv[0]), file=sys.stderr)
    exit(1)

c_code = ''
with open(sys.argv[1], 'r') as f:
    code = ''.join(f.readlines())

    for instr in code:
        if instr == '>':
            c_code += C_REP_SHIFT_RIGHT
        elif instr == '<':
            c_code += C_REP_SHIFT_LEFT
        elif instr == '+':
            c_code += C_REP_INCREMENT
        elif instr == '-':
            c_code += C_REP_DECREMENT
        elif instr == '.':
            c_code += C_REP_PRINT
        elif instr == ',':
            c_code += C_REP_READ
        elif instr == '[':
            c_code += C_REP_LOOP_START
        elif instr == ']':
            c_code += C_REP_LOOP_END

to_compile = C_FILE_HEADER + c_code + C_FILE_FOOTER
out_name = os.path.splitext(ntpath.basename(sys.argv[1]))[0]
c_file_path = '/tmp/' + out_name + '.c'

with open(c_file_path, 'w+') as f:
    f.write(to_compile)

code = call(['gcc', '-Wall', '-O3', '-o', out_name, c_file_path],
            stdout=sys.stdout, stderr=sys.stderr)
os.remove(c_file_path)

print('Compilation finished with exit code ' + str(code))
