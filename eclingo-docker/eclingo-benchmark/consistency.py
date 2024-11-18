import gc
import subprocess

import pandas as pd

from constraint import prepare_constraints

def prepare_instance_paths(df):
    paths = []
    for solver_file in df.Instance:
        solver_split = solver_file.split("/")
        path = solver_split[-3]

        filename = "temp_instances/" + path
        paths.append(filename)
    return paths

def get_answer_set_path(path):
    return path + "_answer_set.txt"

def get_constraints_path(path):
    return path + "_constraints.lp"

def get_new_answer_set(path=None):
    if path is None:
        path = "temp_instances/output.txt"
    with open(path, "r") as file:
        lines = file.readlines()
        answer_set = lines[10]
    return answer_set

def add_constraints(answer_set, path):
    constraints_path = get_constraints_path(path)
    answer_set_path = get_answer_set_path(path)

    as_file = open(answer_set_path, "w")
    c_file = open(constraints_path, "w")
    
    as_atoms = answer_set.split()



df = pd.read_csv("matching_instances.txt")
df = df[df["eclingo"] == "SAT"]

instace_paths = prepare_instance_paths(df)
output_file = open("output.txt", "a")
error_file = open("error.txt", "a")
for path in instace_paths:
    command = f"eclingo {path} {get_constraints_path(path)}"
    # subprocess.run([command], shell=True, stdout=output_file, stderr=error_file, timeout=150)
    # gc.collect()
    answer_set = get_new_answer_set()


    print(command)
