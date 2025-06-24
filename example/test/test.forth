_data_
[ 4 5 6 ] 5 VAR mas
"" 4 VAR str
5 VAR len1
0x04 VAR len2

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
    !var_a !var_b
    var_a var_b +
;

_text_

len1 len2 SUM

PRINT_NUM

HALT