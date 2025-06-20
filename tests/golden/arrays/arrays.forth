

_data_
[ 1 2 3 4 ] 4 VAR mas1
[ 1 2 3 4 ] 4 VAR mas2
[ 0 ] 5 VAR mas3
4 VAR len1
4 VAR len2
0x80 VAR input_addr
0x84 VAR output_addr

_func_
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

LOOP
    0 !i len1 < 1
    WHILE
        i len2 <= IF
            i 4 * !tmp
            mas1 tmp + a! @
            mas2 tmp + a! @
            +
            mas3 tmp + a! !
        ELSE
        THEN
    REPEAT

mas3 PRINT_MAS
HALT
