#!/bin/python3

import os
import pathlib
from pathlib import Path

os.system("rm -rf workdir")

is_ok = True
for in_file in Path("./ins").glob("**/*.ins"):
    print(f"\nTesting {in_file}...\n")

    os.makedirs("workdir", exist_ok = True)
    file_name = os.path.basename(in_file)
    in_path = f"workdir/{file_name}"
    out_path = in_path[:-4] + ".output"
    os.system(f"cp {in_file} {in_path}")

    os.system(f"./insc_llvm {in_path}")
    os.system(f"./insc_jvm {in_path}")

    ll_path = in_path[:-4] + ".ll"
    bc_path = in_path[:-4] + ".bc"
    j_path = in_path[:-4] + ".j"
    class_path = in_path[:-4] + ".class"
    class_name = file_name[:-4]

    if os.system(f"lli {ll_path} > workdir/ll.out") != 0:
        print("ERROR: Running .ll file failed")
        is_ok = False
        break

    if os.system(f"lli {bc_path} > workdir/bc.out") != 0:
        print("ERROR: Running .bc file failed")
        is_ok = False
        break
    
    if os.system(f"java --class-path workdir {class_name} > workdir/class.out") != 0:
        print("ERROR: Running .class file failed")
        is_ok = False
        break

    if os.system(f"python3 instant_interpreter.py {in_path}> workdir/good.out") != 0:
        print("ERROR: Running the interpreter failed - the test must be wrong")
        is_ok = False
        break

    if os.system("diff workdir/good.out workdir/ll.out") != 0:
        print("ERROR: workdir/good.out and workdir/ll.out differ")
        is_ok = False
        break

    if os.system("diff workdir/good.out workdir/bc.out") != 0:
        print("ERROR: workdir/good.out and workdir/bc.out differ")
        is_ok = False
        break

    if os.system("diff workdir/good.out workdir/class.out") != 0:
        print("ERROR: workdir/good.out and workdir/class.out differ")
        is_ok = False
        break

    os.system("rm -r workdir")

if is_ok:
    print("\n\n\nOKKKKKKKKKKKKKKKKKKk\n\n\n")