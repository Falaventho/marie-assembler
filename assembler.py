import re
import sys


def parseargs():
    if len(sys.argv) < 2:
        helpexit()

    source_path = sys.argv[1]

    if source_path == "help" or source_path == "-h":
        helpexit()

    if len(sys.argv) == 2:
        target_path = "MARIE.ROM"
    else:
        target_path = sys.argv[2] + ".ROM"

    return (source_path, target_path)


def helpexit():
    print("Usage: python assembler.py <source file path> <target file path>.")
    exit()


def main():

    source_path, target_path = parseargs()

    # Read the file into a buffer
    with open(source_path, 'r') as file:
        buffer = file.read()

    # Split the buffer into chunks by line, removing blank lines and stripping whitespace
    buffer = re.split("\n+", buffer)
    buffer = [line.strip() for line in buffer]

    # Split each chunk into words by spaces or symbols as appropriate
    for idx in range(len(buffer)):
        chunk = buffer[idx]
        line_end = chunk.find(";")
        if line_end != -1:
            chunk = chunk[:line_end]
        chunk = chunk.strip()
        buffer[idx] = re.split(" +", chunk)

    # Clean up empty lines
    cleaned_lines = [line for line in buffer if line != [""]]

    # Reference collections
    symbols = {}
    instructions = ["JNS", "LOAD", "STORE", "ADD", "SUBT", "INPUT", "OUTPUT",
                    "HALT", "SKIPCOND", "JUMP", "CLEAR", "ADDI", "JUMPI", "LOADI", "STOREI"]
    radices = {
        "DEC": lambda x: int(x),
        "HEX": lambda x: int(x, 16),
        "BIN": lambda x: int(x, 2),
        "OCT": lambda x: int(x, 8),
    }

    # First pass: collect labels and their addresses
    for idx, line in enumerate(cleaned_lines):
        if line[0].endswith(","):
            label = line[0][:-1]
            symbols[label] = idx
            cleaned_lines[idx][0] = label

            if line[1] not in radices:
                raise Exception(f"Unsupported radix on line {idx}: {line[1]}")

            line[2] = radices[line[1]](line[2])

    # Second pass: generate hex code
    hex_code = ""
    for line in cleaned_lines:
        if line[0] in instructions:
            opcode = instructions.index(line[0])
            operand = 0
            if len(line) > 1:
                if line[1] in symbols:
                    operand = symbols[line[1]]
                else:
                    operand = int(line[1])
            hex_line = (opcode << 12) | operand
            hex_code += f"{hex_line:04X}"
        elif line[0] in symbols:
            operand = line[2]
            hex_code += f"{operand:04X}"

    # Convert hex to bytes
    binary_dat = bytes.fromhex(hex_code)

    # Output the binary data
    with open(target_path, 'wb') as f:
        f.write(binary_dat)


if __name__ == "__main__":
    main()
