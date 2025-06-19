_data_
"Hello world" VAR str
0x84 VAR output_addr

_func_
: PRINT
    !iter
    LOOP
        1 !tmp 0 != 0
        WHILE
            3 iter - a! @
            0xFF000000 and
            dup dup !tmp
            0 = IF
            ELSE
                output_addr a! !
                iter 1 + !iter
            THEN
        REPEAT
;

_text_
&str PRINT
HALT
