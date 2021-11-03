#!/bin/python3

import os
import pathlib
from pathlib import Path

jasmin_path = "lib/jasmin.jar"

os.system("rm -rf workdir")

is_ok = True
for in_file in Path("./ins").glob("**/*.ins"):
    print(f"\nTesting {in_file}...\n")

    os.makedirs("workdir", exist_ok = True)
    file_name = os.path.basename(in_file)
    in_path = f"workdir/{file_name}"
    out_path = in_path[:-4] + ".output"
    os.system(f"cp {in_file} {in_path}")

    os.system(f"./insc_jvm {in_path}")

    j_path = in_path[:-4] + ".j"
    class_path = in_path[:-4] + ".class"
    class_name = file_name[:-4]

    j_file = open(j_path).read()
    j_file_less_stack = ""
    j_file_less_vars = ""

    for j_line in j_file.split('\n'):
        if '.limit stack' in j_line:
            stack_limit = int(j_line.split(' ')[-1])
            j_file_less_stack += j_line.replace(str(stack_limit), str(stack_limit - 1)) + "\n"
            j_file_less_vars += j_line + "\n"
            continue

        if '.limit locals' in j_line:
            locals_limit = int(j_line.split(' ')[-1])
            j_file_less_stack += j_line + "\n"
            j_file_less_vars += j_line.replace(str(locals_limit), str(locals_limit - 1)) + "\n"
            continue

        j_file_less_stack += j_line + "\n"
        j_file_less_vars += j_line + "\n"


    if stack_limit != 0:
        open(j_path, "w").write(j_file_less_stack)
        os.system(f"java -jar {jasmin_path} -d workdir {j_path}")

        if os.system(f"java --class-path workdir {class_name} > /dev/null") == 0:
            print(f"ERROR: .limit stack is too large - running with .limit stack {stack_limit-1} didn't crash")
            is_ok = False
            break

    open(j_path, "w").write(j_file_less_vars)
    os.system(f"java -jar {jasmin_path} -d workdir {j_path}")

    if os.system(f"java --class-path workdir {class_name} > /dev/null") == 0:
        print(f"ERROR: .limit locals is too large - running with .limit locals {locals_limit-1} didn't crash")
        is_ok = False
        break

    os.system("rm -r workdir")

if is_ok:
    print("\n\n\nOKKKKKKKKKKKKKKKKKKk\n\n\n")