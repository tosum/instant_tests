#!/bin/python3

# Generates random instant programs
# No division because it breaks stuff

num_to_generate = 10
max_statements = 10
max_constant = 10
max_tree_depth = 5

out_dir = "tests/random/changeme"

import os
import sys
import random

if len(sys.argv) >= 2:
    out_dir = sys.argv[1]

if len(sys.argv) >= 3:
    num_to_generate = int(sys.argv[2])

if len(sys.argv) >= 4:
    max_tree_depth = int(sys.argv[3])

if len(sys.argv) >= 5:
    max_statements = int(sys.argv[4])

if len(sys.argv) >= 6:
    max_constant = int(sys.argv[5])

def generate_expression(available_variables, max_depth_left):
    if random.choice([True, False]):
        max_depth_left -= 1

    if random.randint(0, 5) == 1:
        max_depth_left //= 2

    if max_depth_left == 0:
        max_depth_left = 1

    if max_depth_left == 1:
        if random.choice([True, False]) and len(available_variables) > 0:
            return random.choice(available_variables)
        else:
            return str(random.randint(0, max_constant))

    left = generate_expression(available_variables, max_depth_left - 1)
    right = generate_expression(available_variables, max_depth_left - 1)
    operator = random.choice(['+', "-", "*"])

    my_expr = left + " " + operator + " " + right

    if random.choice([True, False]):
        my_expr = "(" + my_expr + ")"

    return my_expr

def generate_program():
    variables = []

    result = ""
    num_statements = random.randint(0, max_statements)
    for s in range(num_statements):
        expr = generate_expression(variables, max_tree_depth)

        if random.choice([True, False]):
            result += expr + ";\n"
        else:
            if random.choice([True, False]) and len(variables) > 0:
                variable = random.choice(variables)
            else:
                variable = "v" + str(len(variables))
                variables.append(variable)

            result += variable + " = " + expr + ";\n"
            
    return result


os.system("rm -rf workdir")
os.makedirs("workdir", exist_ok = True)

num_generated = 0
while num_generated < num_to_generate:
    program = generate_program()

    if program == "":
        continue

    program += str(random.randint(0, 123)) + "\n" # Dont end with semicolon, put a number there

    open("workdir/random.ins", "w").write(program)

    if os.system("python3 instant_interpreter.py workdir/random.ins > workdir/random.output") != 0:
        continue

    output = open("workdir/random.output").readlines()
    overflow = False
    for line in output:
        val = int(line)

        if val > 2147483647 or val < -2147483648:
            overflow = True
            break

    if overflow:
        print("overflow! trying again...")
        continue
            
    test_id = random.randint(0, 4242)
    test_name = "random" + f"{test_id}.ins"
    open(os.path.join(out_dir, test_name), "w").write(program)

    num_generated += 1
    print(f"Generated {num_generated}/{num_to_generate}")

os.system("rm -rf workdir")
