import re
import sys

ARRAY_SIZE = 30000

# Initialize play area
cells = [0] * ARRAY_SIZE
# Pointer to the cell in use
pointer = 0
# Position in the code
cursor = 0
# Keep track of the start of the loops for faster jumps
queue_jump = []

# Read code from stdin & cleanup comments
data = "".join(sys.stdin.readlines())
data = re.sub(r'[^+\-<>\[\].,]', '', data)

END_POS = len(data)

while not cursor == END_POS:
    instr = data[cursor]

    # Increment current cell
    if instr == '+':
        cells[pointer] += 1
        cells[pointer] %= 0xff

    # Decrement current cell
    elif instr == '-':
        cells[pointer] -= 1
        cells[pointer] %= 0xff

    # Move the pointer to the left
    elif instr == '<':
        pointer -= 1
        pointer %= ARRAY_SIZE

    # Move the pointer to the right
    elif instr == '>':
        pointer += 1
        pointer %= ARRAY_SIZE

    # If current cell is 0, fast forward to ']'
    elif instr == '[':

        # Cell is 0, ignore block
        if cells[pointer] == 0:

            # Fast forward to corresponding ']'
            # Depth is the amount of sub loop encountered to avoid exiting at the wrong ']'
            depth = 0

            # Move one forward manually
            cursor += 1
            instr = data[cursor]

            while not (instr == ']' and depth == 0) or cursor == END_POS:
                if instr == ']':
                    depth -= 1
                elif instr == '[':
                    depth += 1

                # Move to the next instruction
                cursor += 1
                instr = data[cursor]

        # Cell is not 0, run the block
        else:
            # Save the start of the block for faster jump
            queue_jump.append(cursor)

    # If current cell is not 0, jump to the corresponding '['
    elif instr == ']':

        # If not 0, loop
        if not cells[pointer] == 0:
            # Jump to the opening bracket
            cursor = queue_jump[-1]

        # Cell is 0, exit loop
        else:
            # Remove jump point
            queue_jump.pop()

    # Print the ASCII character corresponding to the
    elif instr == '.':
        print(chr(cells[pointer]), end='', file=sys.stdout)

    # Read a byte from stdin & store in the cell
    elif instr == ',':
        cells[pointer] = ord(input('')[0])

    cursor += 1
