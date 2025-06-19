_data_
0 VAR count
0x100 VAR mas
0 VAR len
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
: SORT
    0 !n
    0 !tmp
    LOOP
        0 !i len < 1
        WHILE
            1 i len - - !n
            LOOP
                0 !j n < 1
                WHILE
                    j 4 * !tmp
                    mas tmp + a! @
                    mas tmp 4 + + a! @
                    > IF
                         mas tmp + a! @
                         mas tmp 4 + + a! @
                         over
                         mas tmp 4 + + a! !
                         mas tmp + a! !
                    ELSE
                    THEN
                REPEAT
        REPEAT
;

_text_
mas READ_MAS !len
SORT
mas PRINT_MAS

HALT
