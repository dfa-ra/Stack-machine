_import_
    "../lib/num.forth"

_data_
[ 1 2 3 4 ] 4 VAR mas1
[ 1 2 3 4 ] 4 VAR mas2
[ 0 ] 5 VAR mas3
4 VAR len1
4 VAR len2

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
