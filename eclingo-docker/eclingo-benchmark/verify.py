import os
import glob

def check_output(dir_path_1: str, dir_path_2: str) -> bool:
    """
    Checks the satisfiability based on the saved output file
    """
    
    debug_dict_1 = get_all_sat_checks(dir_path_1)
    debug_dict_2 = get_all_sat_checks(dir_path_2)
    verify_all_instances(debug_dict_1, debug_dict_2)

def get_all_sat_checks(dir_path):
    if not os.path.exists(dir_path):
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
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"{output_file} does not exist!!")
    
    with open(output_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(("SAT", "SATISFIABLE")):
                return True
            elif line.startswith(("UNSAT", "UNSATISFIABLE")):
                return False
        return None

def verify_all_instances(debug_dict_1, debug_dict_2):
    if debug_dict_1 == debug_dict_2:
        print("Output is correct.")
    else:
        print("Output is not correct!!")

    with open("debug_file.txt", "w") as file:
        for output_file in debug_dict_1:
            file.write(f"{output_file}, {debug_dict_1[output_file]}, {debug_dict_2[output_file]}\n")
            if not debug_dict_1[output_file] == debug_dict_2[output_file]:
                print(f"{output_file} not verified!!")
                return
        print("All instances verified.")

def main():
    solver_1 = "eclingo"
    solver_2 = "eclingo-old"
    dest_dir_1 = f"running/benchmark-tool-{solver_1}/output/project/zuse/results/suite/"
    dest_dir_2 = f"running/benchmark-tool-{solver_2}/output/project/zuse/results/suite/"
    check_output(dest_dir_1, dest_dir_2)

if __name__ == "__main__":
    main()