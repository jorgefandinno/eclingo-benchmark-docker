import os
import glob
import shutil

import pandas as pd


def get_as_atoms(answer_set, delimiter=None):
    if delimiter is None:
        return [atom.strip() for atom in answer_set.split() if atom]
    else:
        return [delimiter+atom.strip() for atom in answer_set.split("&") if atom]

def check_output(solver: str) -> bool:
    """
    Checks the satisfiability output for the solvers
    """
    df = pd.read_csv("matching_instances.txt")
    df = df[df["eclingo"] == "SAT"]
    for solver_file in df.Instance:
        solver_split = solver_file.split("/")
        filepath = "/".join(solver_split[1:-2])

        filename = copy_instance(filepath, solver)
        answer_set = get_answer_set(solver, solver_file)
        as_atoms = get_as_atoms(answer_set)
        with open(f"{filename}_answer_set.txt", "w") as file:
            file.writelines(map(lambda x: x + "\n", as_atoms))
        
        constraints = prepare_constraints(as_atoms)
        with open(f"{filename}_constraints.lp", "w") as file:
            file.writelines(map(lambda x: x + "\n", constraints))

def copy_instance(filepath, solver):
    instance_path = os.path.join(os.getcwd(), f"running/benchmark-tool-{solver}/experiments/instances", filepath)
    os.makedirs("temp_instances", exist_ok=True)
    filename = shutil.copy(instance_path, os.path.join("temp_instances", os.path.split(filepath)[-1]))
    return filename

def get_answer_set(solver, solver_file):
    path = os.path.join(os.getcwd(), 
                        f"running/benchmark-tool-{solver}/output/project/zuse/results/suite/", 
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
    solver = "eclingo"
    check_output(solver)

if __name__ == "__main__":
    main()