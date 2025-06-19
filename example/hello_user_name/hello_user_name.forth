_import_
    "../lib/str.forth"

_data_
"" 31 VAR buffer
"What is your name?" VAR question
"Hello, " VAR greeting


_text_
&question PRINT

&buffer READ

&greeting PRINT
&buffer PRINT


HALT
