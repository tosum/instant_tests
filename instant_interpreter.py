#!/bin/python3

import sys

ins_code = open(sys.argv[1]).read()
ins_code = ins_code.replace('\n', '')
ins_code = ins_code.replace(' ', '')
ins_code = ins_code.replace('\r', '')
ins_code = ins_code.replace('\t', '')

python_code = ""
for ins_statement in ins_code.split(';'):
    # Replace / with // - instant does integer division
    python_statement = ins_statement.replace("/", "//")

    if python_statement == "":
        continue

    if '=' in python_statement:
        python_code += f"{python_statement}\n"
    else:
        python_code += f"print({python_statement})\n"

exec(python_code)
