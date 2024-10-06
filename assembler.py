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

    debug = "--debug" in sys.argv

    return (source_path, target_path, debug)


def helpexit():
    print(
        "Usage: python assembler.py <source file path> <target file path> [--debug].")
    exit()


def main():

    source_path, target_path, debug = parseargs()
    memory_offset = 0

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
        "CHAR": lambda x: ord(x)
    }
    directives = ["ORG"]

    # First pass: collect labels and their addresses - process directives
    idx = 0
    while idx < len(cleaned_lines):
        line = cleaned_lines[idx]
        if line[0].endswith(","):
            label = line[0][:-1]
            symbols[label] = idx + memory_offset
            cleaned_lines[idx] = line[1:]

            # if line[1] not in radices:
            #     raise Exception(f"Unsupported radix on line {idx}: {line[1]}")

            # line[2] = radices[line[1]](line[2])

        if line[0] in directives:
            match line[0]:
                case "ORG":
                    memory_offset = int(line[1])
            cleaned_lines.pop(idx)
        idx += 1

    # Second pass: generate hex code
    hex_code = "" + ("0000" * memory_offset)
    for line in cleaned_lines:
        if line[0] in instructions:
            opcode = instructions.index(line[0])
            operand = 0
            if len(line) > 1:
                if line[1] in symbols:
                    operand = symbols[line[1]]
                else:
                    operand = int(line[1], 16)

            hex_line = (opcode << 12) | operand
            hex_code += f"{hex_line:04X}"
            if debug:
                print(f"Instruction: {line[0]}, Operand: " +
                      f"{operand}, Hex: {hex_line:04X}")
        elif line[0] in radices:
            value = radices[line[0]](line[1])
            hex_code += f"{value:04X}"
        else:
            raise Exception(f"Unidentified symbol found in {line}")

    # Convert hex to bytes
    binary_dat = bytes.fromhex(hex_code)

    # Output the binary data
    with open(target_path, 'wb') as f:
        f.write(binary_dat)

    if debug:
        print(f"Final Hex Code: {hex_code}")


if __name__ == "__main__":
    main()
