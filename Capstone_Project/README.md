# Nand2Tetris-I Capstone — Roll No. 2501730015

Personal number: K = 15
- K mod 3 = 0: assembler exports labels and variables to `symbols.txt`.
- K mod 4 = 3: box width = 16 × 4 = 64 pixels.
- Box starts at screen row 15 and is 20 rows tall.

## Files
- `CPU.hdl`, `Memory.hdl`, `Computer.hdl`: Hack computer integration.
- `assembler.py`: two-pass Hack assembler with symbol-table export.
- `Box.asm`: keyboard-controlled 64 × 20 pixel box.
- `Box.hack`: generated machine code.
- `symbols.txt`: labels and variables with addresses.

## Assemble
From this folder:
```bash
python assembler.py Box.asm
```
This writes `Box.hack` and `symbols.txt`.

## Verify
Open the Nand2Tetris Hardware Simulator and run the official CPU/Memory/Computer test scripts.
Open the CPU Emulator, load `Box.hack`, run it, press/release a key and capture the display.
Do not claim a test passed until it has actually been run in the simulator.

## Note
The HDL files use standard built-in Hack components for the ALU, registers, PC, RAM, Screen, Keyboard and ROM. If your course environment requires your own lower-level chip implementations, those chips must be added and tested separately.
