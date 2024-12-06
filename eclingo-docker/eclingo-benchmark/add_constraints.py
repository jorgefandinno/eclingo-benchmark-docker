import os
import shutil

import pandas as pd

from constraint_utils import (
    prepare_constraints, 
    get_as_atoms, 
    write_to_file,
    get_answer_set_path,
    get_constraints_path
)


def check_output(solver: str) -> bool:
    """
    Checks the satisfiability output for the solvers
    and write answer sets and constraints to files
    """
    df = pd.read_csv("matching_instances.txt")
    df = df[df["eclingo"] == "SAT"]
    for solver_file in df.Instance:
        solver_split = solver_file.split("/")
        filepath = "/".join(solver_split[1:-2])

        instance_path = get_instance_path(filepath, solver)
        dest_path = get_destination_path("temp_instances", filepath)
        filename = copy_instance(instance_path, dest_path)

        answer_set = get_answer_set(solver, solver_file)
        as_atoms = get_as_atoms(answer_set)
        as_path = get_answer_set_path(filename)
        write_to_file(as_path, as_atoms, replace=True)
        
        constraints = prepare_constraints(as_atoms)
        constraint_path = get_constraints_path(filename)
        write_to_file(constraint_path, constraints, replace=True)

def get_instance_path(filepath, solver):
    return os.path.join(
        os.getcwd(), 
        f"running/benchmark-tool-{solver}/experiments/instances", 
        filepath
    )

def get_destination_path(dir, filepath):
    os.makedirs(dir, exist_ok=True)
    return os.path.join(dir, os.path.split(filepath)[-1])
 
def copy_instance(instance_path, dest_path):
    filename = shutil.copy(instance_path, dest_path)
    return filename

def get_answer_set(solver, solver_file):
    path = os.path.join(
        os.getcwd(), 
        f"running/benchmark-tool-{solver}/output/project/zuse/results/suite/", 
        solver_file
    )
    with open(path, "r") as file:
        lines = file.readlines()
        answer_set = lines[10]
    return answer_set

def main():
    solver = "eclingo"
    check_output(solver)

if __name__ == "__main__":
    main()