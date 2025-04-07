import os
import glob

from typing import Tuple

from .constraint_utils import match_files, check_sat


def check_output_satisfiability(solver_1: str, solver_2: str, s1_results_path: str, s2_results_path: str) -> bool:
    """
    Checks the satisfiability output for the solvers
    """
    solver_1_output = get_all_sat_checks(s1_results_path)
    solver_2_output = get_all_sat_checks(s2_results_path)

    solver_output = ((solver_1, solver_1_output), (solver_2, solver_2_output))
    check_all_instances(solver_output, match_files)

def get_all_sat_checks(dir_path: str):
    if not os.path.isdir(dir_path):
        raise NotADirectoryError(f"The {dir_path} is not a directory.")
    
    debug_dict = {}
    for folder in glob.glob(f"{dir_path}/script-0-*"):
        for bp in glob.glob(f"{folder}/*"):
            for instance in glob.glob(f"{bp}/*"):
                if os.path.isdir(f"{instance}/run1/"):
                    debug_dict.update(get_sat(instance))
                else:
                    for inst in glob.glob(f"{instance}/*"):
                        debug_dict.update(get_sat(inst))

    return debug_dict

def get_sat(path):
    output_file = f"{path}/run1/runsolver.solver"
    if not os.path.exists(output_file):
        return {}
    
    sat = check_sat(output_file)
    output_file_split = output_file.split("/")

    if output_file_split[-6].startswith("script"):
        new_file_name = os.path.join(*output_file_split[-6:])
    else:
        new_file_name = os.path.join(*output_file_split[-5:])

    return {new_file_name: sat}

def check_all_instances(solver_output: Tuple[Tuple, Tuple], match_files: Tuple):
    ((solver_1, solver_1_output), (solver_2, solver_2_output)) = solver_output

    if solver_1_output == solver_2_output:
        print("Consistent SAT and UNSAT across both solvers.")
    else:
        print(solver_1_output)
        print(solver_2_output)
        print("Satisfiability is not consistent !!")

    match_file = open_file(match_files[0], (solver_1, solver_2))
    non_match_file = open_file(match_files[1], (solver_1, solver_2))
    timed_out_file = open_file(match_files[2], (solver_1, solver_2))
    
    for output_file in solver_1_output:
        if not all((solver_1_output[output_file], solver_2_output[output_file])):
            timed_out_file.write(f"{output_file},{solver_1_output[output_file]},{solver_2_output[output_file]}\n")
        elif solver_1_output[output_file] == solver_2_output[output_file]:
            match_file.write(f"{output_file},{solver_1_output[output_file]},{solver_2_output[output_file]}\n")
        else:
            non_match_file.write(f"{output_file},{solver_1_output[output_file]},{solver_2_output[output_file]}\n")
            print(f"{output_file} not verified!!")
    
    match_file.close()
    non_match_file.close()
    timed_out_file.close()

def open_file(file_name: str, solvers: Tuple[str, str]):
    file = open(file_name, "w")
    solver_1, solver_2 = solvers
    file.write(f"instance,{solver_1},{solver_2}\n")
    return file

