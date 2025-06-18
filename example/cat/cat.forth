_data_
"Hello world" VAR str
0x80 VAR input_addr
0x84 VAR output_addr
0 VAR iter

_func_
: PRINT
    !iter
    LOOP
        1 !tmp 0 != 0
        WHILE
            iter a! @
            0xFF000000 and
            dup !tmp
            output_addr a! !
            iter 1 + !iter
        REPEAT
;

_text_
*str PRINT
HALT
