_data_

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

: PRINT_NUM
    output_addr a! !
;

: READ_NUM
    input_addr a! @
;


