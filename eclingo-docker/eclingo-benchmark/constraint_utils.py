import os

from typing import List

def get_answer_set_path(path):
    return path + "_answer_set.txt"

def get_constraints_path(path):
    return path + "_constraints.lp"

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
    if delimiter is None:
        return [atom.strip().replace(" ", "") for atom in answer_set.split() if atom]
    else:
        return [delimiter+atom.strip().replace(" ", "") for atom in answer_set.split("&") if atom]
    

def replace_constraints(filepath, new_atoms):
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
        os.remove(filepath)

    with open(filepath, "a") as file:
        if new_line:
            file.writelines(map(lambda x: x + "\n", write_list))
        else:
            file.writelines(write_list)
