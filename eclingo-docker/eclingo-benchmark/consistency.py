import gc
import re
import subprocess

import pandas as pd

from verify import check_sat


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

def get_new_answer_set(line_index, path=None):
    if path is None:
        path = "output.txt"
    with open(path, "r") as file:
        lines = file.readlines()
        answer_set = lines[line_index]
    return answer_set

def get_as_atoms(answer_set, delimiter=None):
    if delimiter is None:
        return [re.sub(" ", "", atom.strip()) for atom in answer_set.split() if atom]
    else:
        return [re.sub(" ", "", delimiter+atom.strip()) for atom in answer_set.split("&") if atom]


def add_constraints(new_answer_set, path, delimiter=None):
    new_as_atoms = set(get_as_atoms(new_answer_set, delimiter))

    old_answer_set_path = get_answer_set_path(path)
    with open(old_answer_set_path, "r") as file:
        old_answer_set = file.read()
    
    old_as_atoms = set(get_as_atoms(old_answer_set, delimiter))

    new_atoms = new_as_atoms - old_as_atoms
    if not new_atoms:
        print("Same answer set achieved.")
        return False
    
    constraint_path = get_constraints_path(path)
    with open(constraint_path, "a") as file:
        for atom in new_atoms:
            file.write(f":- {atom}.\n")
    
    return True


def main():
    df = pd.read_csv("matching_instances.txt")
    df = df[df["eclingo"] == "SAT"]

    instace_paths = prepare_instance_paths(df)
    for path in instace_paths:
        print(path)
        # if not path.startswith("temp_instances/yale"):
        #     continue

        while True:
            command = f"eclingo {path} {get_constraints_path(path)}"

            output_file = open("output.txt", "w")
            error_file = open("error.txt", "w")
            subprocess.run([command], shell=True, stdout=output_file, stderr=error_file, timeout=150)
            gc.collect()
            output_file.close()
            error_file.close()

            sat = check_sat("output.txt")
            if sat != "SAT":
                print("Does not have same answer set.")
                break

            answer_set = get_new_answer_set(line_index=3)
            if not add_constraints(answer_set, path, delimiter="&"):
                break
        
        break

    print("Done.")

if __name__ == "__main__":
    main()
