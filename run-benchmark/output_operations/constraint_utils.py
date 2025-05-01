import os

from typing import List
from .parameters import answer_line_indices, relative_indices

match_files = (
    "matching_instances.txt",
    "non_matching_instances.txt",
    "timed_out_instances.txt"
)

def get_answer_set_path(path):
    return path + "_answer_set.txt"

def get_constraints_path(path):
    return path + "_constraints.lp"

def find_line_index(path, text):
    with open(path, "r") as file:
        lines = file.readlines()
        
    for idx, line in enumerate(lines):
        if text.lower() in line.lower():
            return idx

    print("Error on finding answer set line index.")
    exit(1)

def find_answer_line_index(solver, path):
    answer_line_index = answer_line_indices.get(solver)
    if not answer_line_index and not relative_indices.get(solver):
        print(f"Could not find answer line index for {solver}. Please check the parameters file.")
        exit(1)
            
    if not answer_line_index:
        text, deviation = relative_indices[solver]
        answer_line_index = find_line_index(path, text) + deviation
    
    return answer_line_index

def check_sat(path: str):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"{path} does not exist!!")

    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(("SAT", "SATISFIABLE")):
                return "SAT"
            elif line.startswith(("UNSAT", "UNSATISFIABLE")):
                return "UNSAT"
        return None

def prepare_constraints(atoms: List[str], negative: bool=True):
    constraints = []
    for atom in atoms:
        #check for negative atom in answer set
        if atom.startswith("&k{~"):
            continue

        if negative:
            constraints.append(f":- not {atom}.")
        else:
            constraints.append(f":- {atom}.")
            
    return constraints

def get_as_atoms(answer_set, delimiter=None):
    if not delimiter:
        return [atom.strip().replace(" ", "") for atom in answer_set.split() if atom]
    else:
        return [delimiter+atom.strip().replace(" ", "") for atom in answer_set.split(delimiter) if atom]
    

def replace_constraints(filepath, new_atoms):
    """
    This function is used for testing eclingo variants
    """
    with open(filepath, "r") as file:
        content = file.read()
    
    filtered_atoms = set()
    for atom in new_atoms:
        if atom.startswith("&k{") and not atom.startswith("&k{~"):
            atom_check = "&m{" + atom.replace("&k{", "")

            if content.find(atom) != -1 or content.find(atom_check) != -1:
                content = content.replace(atom_check, atom)
            else:
                filtered_atoms.add(atom)
    
    with open(filepath, "w") as file:
        file.write(content)
    
    return filtered_atoms


def write_to_file(filepath, write_list, new_line=True, replace=False):
    if replace:
        try:
            os.remove(filepath)
        except FileNotFoundError:
            pass

    with open(filepath, "a") as file:
        if new_line:
            file.writelines(map(lambda x: x + "\n", write_list))
        else:
            file.writelines(write_list)
