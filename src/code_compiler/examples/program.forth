_import_
    "lib/str.forth"

_data_
0 VAR test
"Hello world" VAR str
0x80 VAR input_addr
0x84 VAR output_addr

_text_
&str PRINT
HALT
