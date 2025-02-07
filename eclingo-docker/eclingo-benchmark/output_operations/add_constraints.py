import os
import shutil

import pandas as pd

from .constraint_utils import (
    match_files,
    prepare_constraints, 
    get_as_atoms, 
    write_to_file,
    get_answer_set_path,
    get_constraints_path
)


def save_constraints(solver: str, results_path: str, rel_instance_path: str, line_number: int) -> bool:
    """
    Checks the satisfiability output for the solvers
    and write answer sets and constraints to files
    """
    df = pd.read_csv(match_files[0])
    df = df[df[solver] == "SAT"]
    for solver_file in df.Instance:
        solver_split = solver_file.split("/")
        filepath = "/".join(solver_split[1:-2])

        instance_path = get_instance_path(filepath, rel_instance_path)
        dest_path = get_destination_path("temp_instances", filepath)
        filename = copy_instance(instance_path, dest_path)

        answer_set = get_answer_set(results_path, solver_file, line_number)
        as_atoms = get_as_atoms(answer_set)
        as_path = get_answer_set_path(filename)
        write_to_file(as_path, as_atoms, replace=True)
        
        constraints = prepare_constraints(as_atoms)
        constraint_path = get_constraints_path(filename)
        write_to_file(constraint_path, constraints, replace=True)

def get_instance_path(filepath, rel_instance_path):
    return os.path.join(
        os.getcwd(), 
        rel_instance_path, 
        filepath
    )

def get_destination_path(dir, filepath):
    os.makedirs(dir, exist_ok=True)
    return os.path.join(dir, os.path.split(filepath)[-1])
 
def copy_instance(instance_path, dest_path):
    filename = shutil.copy(instance_path, dest_path)
    return filename

def get_answer_set(results_path, solver_file, line_number):
    path = os.path.join(
        os.getcwd(), 
        results_path, 
        solver_file
    )
    with open(path, "r") as file:
        lines = file.readlines()
        answer_set = lines[line_number]
    return answer_set

