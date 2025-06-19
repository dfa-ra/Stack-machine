_import_
    "../lib/num.forth"

_data_
0 VAR count
0x100 VAR mas
0 VAR len

_func_
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
