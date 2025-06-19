_import_
    "../../lib/num.forth"

_data_
0 VAR count
0x100 VAR mas1
0x130 VAR mas2
0x160 VAR mas3
0 VAR len1
0 VAR len2

_func_

_text_
mas1 READ_MAS !len1
mas2 READ_MAS !len2

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