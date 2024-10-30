import os
import glob
import shutil

import pandas as pd


def check_output(solver_1: str) -> bool:
    """
    Checks the satisfiability output for the solvers
    """
    df = pd.read_csv("matching_instances.txt")
    df = df[df[" eclingo"] == " SAT"]
    for solver_file in df.Instance:
        solver_split = solver_file.split("/")

        if solver_split[-5].startswith("script"):
            filepath = "/".join(solver_split[-4:-2]) 
        elif solver_split[-6].startswith("script"):
            filepath = "/".join(solver_split[-5:-2]) 
        else:
            filepath = solver_split[-3]

        filename = copy_instance(filepath)
        answer_set = get_answer_set(solver_1, solver_file)
        as_atoms = answer_set.split()
        constraints = prepare_constraints(as_atoms)
        with open(filename, "a") as file:
            file.writelines(constraints)

def copy_instance(filepath):
    instance_path = os.path.join(os.getcwd(), "running/benchmark-tool-{solver_1}/experiments/instances", filepath)
    os.makedirs("temp_instances", exist_ok=True)
    filename = shutil.copy(instance_path, os.path.join("temp_instances", os.path.split()[-1]))
    return filename

def get_answer_set(solver_1, solver_file):
    path = os.path.join(os.getcwd(), 
                        f"running/benchmark-tool-{solver_1}/output/project/zuse/results/suite/", 
                        solver_file)
    with open(path, "r") as file:
        lines = file.readlines()
        answer_set = lines[10]
    return answer_set

def prepare_constraints(atoms):
    constraints = []
    for atom in atoms:
        constraints.append(f":- not {atom}.")
    return constraints

def main():
    solver_1 = "eclingo"
    check_output(solver_1)

if __name__ == "__main__":
    main()