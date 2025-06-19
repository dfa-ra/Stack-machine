_data_
0 VAR n
0 VAR sum_pow2
0 VAR pow2_sum

0x80 VAR input_addr
0x84 VAR output_addr

_func_
: PRINT_NUM
    output_addr a! !
;
: READ_NUM
    input_addr a! @
;
: SUM
    LOOP
        1 !j n <= 1
        WHILE
            sum_pow2 j + !sum_pow2
        REPEAT
;
: SUM_POW2
    LOOP
        1 !i n <= 1
        WHILE
            i i * !tmp
            pow2_sum tmp + !pow2_sum
        REPEAT
;


_text_
READ_NUM !n

SUM
sum_pow2 sum_pow2 * !sum_pow2
SUM_POW2
pow2_sum sum_pow2 - !n
@n PRINT_NUM

HALT
