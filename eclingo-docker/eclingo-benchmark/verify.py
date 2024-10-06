import os
import glob

from typing import Tuple


def check_output(solver_1: str, solver_2: str) -> bool:
    """
    Checks the satisfiability output for the solvers
    """
    dir_path_1 = f"running/benchmark-tool-{solver_1}/output/project/zuse/results/suite/"
    dir_path_2 = f"running/benchmark-tool-{solver_2}/output/project/zuse/results/suite/"
    
    solver_1_output = get_all_sat_checks(dir_path_1)
    solver_2_output = get_all_sat_checks(dir_path_2)

    solver_output = ((solver_1, solver_1_output), (solver_2, solver_2_output))
    verify_all_instances(solver_output)

def get_all_sat_checks(dir_path: str):
    if not os.path.isdir(dir_path):
        raise NotADirectoryError(f"The {dir_path} is not a directory.")
    
    debug_dict = {}
    for folder in glob.glob(f"{dir_path}/script-0-*"):
        for bp in glob.glob(f"{folder}/*"):
            for instance in glob.glob(f"{bp}/*"):
                output_file = f"{instance}/run1/runsolver.solver"
                sat = check_sat(output_file)
                output_file_split = output_file.split("/")
                new_file_name = os.path.join(*output_file_split[-5:])
                debug_dict[new_file_name] = sat
    return debug_dict

def check_sat(output_file: str):
    if not os.path.isfile(output_file):
        raise FileNotFoundError(f"{output_file} does not exist!!")
    
    with open(output_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(("SAT", "SATISFIABLE")):
                return True
            elif line.startswith(("UNSAT", "UNSATISFIABLE")):
                return False
        return None

def verify_all_instances(solver_output: Tuple[Tuple, Tuple]):
    ((solver_1, solver_1_output), (solver_2, solver_2_output)) = solver_output

    if solver_1_output == solver_2_output:
        print("Output is consistent across both solvers.")
    else:
        print("Output is not consistent !!")

    match_file = open_file("matching_instances.txt")
    non_match_file = open_file("non_matching_instances.txt")
    
    for output_file in solver_1_output:
        if solver_1_output[output_file] == solver_2_output[output_file]:
            match_file.write(f"{output_file}, {solver_1}, {solver_2}\n")
        else:
            non_match_file.write(f"{output_file}, {solver_1}, {solver_2}\n")
            print(f"{output_file} not verified!!")
    
    match_file.close()
    non_match_file.close()

def open_file(file_name: str):
    file = open(file_name, "w")
    file.write("Instance, Solver1, Solver2\n")
    return file

def main():
    solver_1 = "eclingo"
    solver_2 = "eclingo-old"
    check_output(solver_1, solver_2)

if __name__ == "__main__":
    main()