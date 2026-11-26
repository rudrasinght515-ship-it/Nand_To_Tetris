// Roll number: 2501730339; K=39
// Box: starts at row 39, height 20 rows, width 64 pixels (4 words).
// While any key is pressed, paint black; otherwise clear the same area.

(LOOP)
    @KBD
    D=M
    @DRAW
    D;JGT

// Clear the box: 20 rows x 4 words.
    @SCREEN
    D=A
    @1248
    D=D+A
    @PTR
    M=D
    @20
    D=A
    @ROWS
    M=D

(CLEAR_ROW)
    @4
    D=A
    @COLS
    M=D

(CLEAR_COL)
    @PTR
    A=M
    M=0
    @PTR
    M=M+1
    @COLS
    MD=M-1
    @CLEAR_COL
    D;JGT

    @32
    D=A
    @PTR
    M=D+M
    @4
    D=A
    @PTR
    M=M-D
    @ROWS
    MD=M-1
    @CLEAR_ROW
    D;JGT

    @LOOP
    0;JMP

(DRAW)
// Draw the box: 20 rows x 4 words, each word = 16 black pixels.
    @SCREEN
    D=A
    @1248
    D=D+A
    @PTR
    M=D
    @20
    D=A
    @ROWS
    M=D

(DRAW_ROW)
    @4
    D=A
    @COLS
    M=D

(DRAW_COL)
    @PTR
    A=M
    M=-1
    @PTR
    M=M+1
    @COLS
    MD=M-1
    @DRAW_COL
    D;JGT

    @32
    D=A
    @PTR
    M=D+M
    @4
    D=A
    @PTR
    M=M-D
    @ROWS
    MD=M-1
    @DRAW_ROW
    D;JGT

    @LOOP
    0;JMP