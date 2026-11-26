#!/usr/bin/env python3

"""
Two-pass assembler for the Nand2Tetris Hack computer.

Student Roll Number: 2501730339
K = 39

Extra Feature (K mod 3 = 0):
Save all labels and variables with their addresses
in symbols.txt.

Usage:
python assembler.py input.asm [output.hack]
"""

import re
import sys
from pathlib import Path


# Predefined symbols
PREDEFINED = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
}

PREDEFINED.update({f"R{i}": i for i in range(16)})


# Destination codes
DEST = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "DM": "011",
    "A": "100",
    "AM": "101",
    "MA": "101",
    "AD": "110",
    "DA": "110",
    "AMD": "111",
    "ADM": "111",
    "MAD": "111",
    "MDA": "111",
    "DAM": "111",
    "DMA": "111",
}


# Jump codes
JUMP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


# Computation codes
COMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "A+D": "0000010",
    "D+M": "1000010",
    "M+D": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "A&D": "0000000",
    "D&M": "1000000",
    "M&D": "1000000",
    "D|A": "0010101",
    "A|D": "0010101",
    "D|M": "1010101",
    "M|D": "1010101",
}


# Valid Hack symbol pattern
SYMBOL_PATTERN = r"[A-Za-z_.$:][A-Za-z0-9_.$:]*"


def clean_source(path):
    """Remove comments and blank lines."""

    lines = []

    for original_no, raw in enumerate(
        Path(path).read_text(encoding="utf-8").splitlines(), 1
    ):

        line = raw.split("//", 1)[0].strip()

        if line:
            lines.append(
                (original_no, re.sub(r"\s+", "", line))
            )

    return lines


def assemble(source_path, output_path=None):

    lines = clean_source(source_path)

    symbols = dict(PREDEFINED)

    label_symbols = {}
    variables = {}

    rom = 0

    # ==================================
    # PASS 1: Find labels
    # ==================================

    for line_no, line in lines:

        if line.startswith("(") and line.endswith(")"):

            label = line[1:-1]

            if not re.fullmatch(SYMBOL_PATTERN, label):
                raise ValueError(
                    f"Line {line_no}: invalid label declaration"
                )

            if label in symbols:
                raise ValueError(
                    f"Line {line_no}: duplicate/predefined label '{label}'"
                )

            symbols[label] = rom
            label_symbols[label] = rom

        else:
            rom += 1

    # ==================================
    # PASS 2: Translate instructions
    # ==================================

    machine = []

    next_ram = 16

    for line_no, line in lines:

        if line.startswith("(") and line.endswith(")"):
            continue

        try:

            # A-INSTRUCTION
            if line.startswith("@"):

                token = line[1:]

                if token.isdigit():

                    value = int(token)

                elif token in symbols:

                    value = symbols[token]

                elif re.fullmatch(SYMBOL_PATTERN, token):

                    value = next_ram

                    symbols[token] = value
                    variables[token] = value

                    next_ram += 1

                else:
                    raise ValueError(
                        "invalid A-instruction symbol"
                    )

                if not 0 <= value <= 32767:
                    raise ValueError(
                        "A-instruction value must be 0..32767"
                    )

                machine.append(f"{value:016b}")

                continue

            # C-INSTRUCTION

            dest = ""
            comp_jump = line

            if "=" in line:

                if line.count("=") != 1:
                    raise ValueError(
                        "invalid destination syntax"
                    )

                dest, comp_jump = line.split("=")

            comp = comp_jump
            jump = ""

            if ";" in comp_jump:

                if comp_jump.count(";") != 1:
                    raise ValueError(
                        "invalid jump syntax"
                    )

                comp, jump = comp_jump.split(";")

            if comp not in COMP:
                raise ValueError(
                    f"unknown computation '{comp}'"
                )

            if dest not in DEST:
                raise ValueError(
                    f"invalid destination '{dest}'"
                )

            if jump not in JUMP:
                raise ValueError(
                    f"invalid jump '{jump}'"
                )

            machine.append(
                "111"
                + COMP[comp]
                + DEST[dest]
                + JUMP[jump]
            )

        except ValueError as exc:

            raise ValueError(
                f"Line {line_no}: {exc}"
            ) from exc

    # ==================================
    # WRITE MACHINE CODE
    # ==================================

    if output_path is None:

        output_path = str(
            Path(source_path).with_suffix(".hack")
        )

    Path(output_path).write_text(
        "\n".join(machine) + "\n",
        encoding="utf-8"
    )

    # ==================================
    # EXTRA FEATURE FOR K = 39
    # K mod 3 = 0
    # Export labels and variables
    # ==================================

    symbol_path = Path(output_path).with_name(
        "symbols.txt"
    )

    with symbol_path.open("w", encoding="utf-8") as f:

        f.write("SYMBOL\tADDRESS\tTYPE\n")

        for name, address in sorted(label_symbols.items()):

            f.write(
                f"{name}\t{address}\tLABEL\n"
            )

        for name, address in sorted(variables.items()):

            f.write(
                f"{name}\t{address}\tVARIABLE\n"
            )

    print(
        f"Assembled {len(machine)} instructions -> {output_path}"
    )

    print(
        f"Symbol table saved -> {symbol_path}"
    )


if __name__ == "__main__":

    if len(sys.argv) not in (2, 3):

        print(
            "Usage: python assembler.py input.asm [output.hack]"
        )

        sys.exit(1)

    try:

        assemble(
            sys.argv[1],
            sys.argv[2] if len(sys.argv) == 3 else None
        )

    except (ValueError, OSError) as exc:

        print(f"Error: {exc}")
        sys.exit(1)
