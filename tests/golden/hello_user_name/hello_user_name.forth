
_data_
"" 31 VAR buffer
"What is your name?" VAR question
"Hello, " VAR greeting
0x80 VAR input_addr
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
: READ
    !iter1
    LOOP
        1 !tmp1 0 != 0
        WHILE
            input_addr a! @
            dup !tmp1
            iter1 a! !
            iter1 1 + !iter1
        REPEAT
;


_text_
&question PRINT

&buffer READ

&greeting PRINT
&buffer PRINT

HALT
