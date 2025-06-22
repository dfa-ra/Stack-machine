
_data_
0 VAR count
0x100 VAR mas1
0x130 VAR mas2
0x160 VAR mas3
0 VAR len1
0 VAR len2

0x80 VAR input_addr
0x84 VAR output_addr

_func_
: READ_MAS
    !iter1
    0 !i1
    LOOP
        1 !tmp1 0 != 0
        WHILE
            input_addr a! @
            dup !tmp1
            iter1 a! !
            iter1 4 + !iter1
            1 i1 + !i1
        REPEAT
    1 i1 -
;
: PRINT_MAS
    !iter
    LOOP
        1 !tmp 0 != 0
        WHILE
            iter a! @
            dup dup !tmp
            0 = IF
            ELSE
                output_addr a! !
                iter 4 + !iter
            THEN
        REPEAT
;

_text_
mas1 READ_MAS !len1
mas2 READ_MAS !len2

LOOP
    0 !i len1 < 4
    WHILE
        i len2 <= IF
            i 4 * !tmp
            mas1 tmp + a! v@
            mas2 tmp + a! v@
            v+
            mas3 tmp + a! v!
        ELSE
        THEN
    REPEAT

mas3 PRINT_MAS
HALT