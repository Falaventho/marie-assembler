import re


def main():
    print("Hello, world!")

# TODO Take a file path as input

# TODO Read the file into a buffer


# Placeholder buffer for working
buffer = "LOAD VALUE; testing a comment\nADD TWO\nSTORE RESULT\nHALT; testing a comment\n\nVALUE, 5\nTWO, 2\n RESULT, 0"

# Split the buffer into chunks by line, removing blank lines
buffer = re.split("\n+", buffer)

# TODO strip whitespace from ends of chunks

# Split each chunk into words by spaces or symbols as appropriate
for idx, chunk in buffer.enumerate():
    line_end = chunk.find(";")
    if line_end != -1:
        chunk = chunk[:line_end]
    buffer[idx] = re.split(" +", chunk)


# Clean up empty lines and commented out code.
cleaned_lines = []
for chunk in buffer:
    if chunk == [""]:
        continue
    cleaned_lines.append(chunk)

# TODO Create a symbol table that stores labels and associated addresses (line numbers + start_addr)
symbols = {
    "START": 0
}

# enum Instruction {
#     JnS(i16),
#     Load(i16),
#     Store(i16),
#     Add(i16),
#     Subt(i16),
#     Input,
#     Output,
#     Halt,
#     Skipcond(i16),
#     Jump(i16),
#     Clear,
#     AddI(i16),
#     JumpI(i16),
#     LoadI(i16),
#     StoreI(i16),
# }

instructions = ["JNS", "LOAD", "STORE", "ADD", "SUBT", "INPUT", "OUTPUT",
                "HALT", "SKIPCOND", "JUMP", "CLEAR", "ADDI", "JUMPI", "LOADI", "STOREI"]

for idx, chunk in cleaned_lines.enumerate():
    if chunk[0] in instructions:
        continue
    if chunk[0][-1] == ",":
        symbol = chunk[0][:-1]
        symbols[symbol] = idx
    else:
        raise Exception(f"Unrecognized instruction on line" +
                        f"{idx}: {chunk.join(" ")}")


# TODO Convert instructions into opcodes, folding with attached values if applicable

# TODO Convert symbols into appropriate addresses

# TODO Output a hex string of the final buffer
