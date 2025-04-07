import gc
import subprocess

import pandas as pd

from .constraint_utils import (
    match_files,
    check_sat,
    prepare_constraints, 
    get_as_atoms, 
    write_to_file,
    get_answer_set_path,
    get_constraints_path,
    replace_constraints,
    find_line_index,
)

from .parameters import (
    answer_line_indices,
    delimiters,
    relative_indices,
)


def prepare_instance_paths(df):
    paths = []
    for op_filepath in df.instance:
        path = op_filepath.split("/")[-3]

        filename = "temp_instances/" + path
        if filename not in paths:
            paths.append(filename)
    return paths

def get_new_answer_set(path, line_index):
    with open(path, "r") as file:
        lines = file.readlines()
        answer_set = lines[line_index]
    return answer_set


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
    new_atoms = replace_constraints(constraint_path, new_atoms)
    constraints = prepare_constraints(new_atoms, negative=False)
    if not constraints:
        print("Same answer set achieved.")
        return False

    write_to_file(constraint_path, constraints)
    return True


def check_output_consistency(s2_name, solver_2):
    df = pd.read_csv(match_files[0])
    df = df[df[s2_name] == "SAT"]

    instance_paths = prepare_instance_paths(df)
    for path in instance_paths:

        print(path)

        while True:
            command = f"{solver_2} {path} {get_constraints_path(path)}"

            output_file = open("output.txt", "w")
            error_file = open("error.txt", "w")
            subprocess.run([command], shell=True, stdout=output_file, stderr=error_file, timeout=610)
            gc.collect()
            output_file.close()
            error_file.close()

            sat = check_sat("output.txt")
            if sat != "SAT":
                print("Does not have same answer set.")
                break
            
            new_as_path = "output.txt"
            line_index = answer_line_indices.get(s2_name)
            if not line_index:
                text, deviation = relative_indices[s2_name]
                line_index = find_line_index(path, text) + deviation
                
            answer_set = get_new_answer_set(new_as_path, line_index)
            if not add_constraints(answer_set, path, delimiters.get(s2_name)):
                break

