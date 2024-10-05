import re


def main():
    # Take a file path as input
    source_path = input("Enter the source file path: ")
    target_path = input("Enter the target file path: ")

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

    # Create a symbol table that stores labels and addr
    symbols = {}
    instructions = ["JNS", "LOAD", "STORE", "ADD", "SUBT", "INPUT", "OUTPUT",
                    "HALT", "SKIPCOND", "JUMP", "CLEAR", "ADDI", "JUMPI", "LOADI", "STOREI"]

    # First pass: collect labels and their addresses
    for idx, line in enumerate(cleaned_lines):
        if line[0].endswith(","):
            label = line[0][:-1]
            symbols[label] = idx
            cleaned_lines[idx][0] = label

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
            operand = int(line[1])
            hex_code += f"{operand:04X}"

    # Output the final hex string to file
    with open(target_path, 'w+') as f:
        f.write(hex_code)


if __name__ == "__main__":
    main()
