import os
import shutil

import pandas as pd

from .constraint_utils import (
    match_files,
    prepare_constraints, 
    get_as_atoms, 
    write_to_file,
    get_answer_set_path,
    get_constraints_path,
    find_answer_line_index,
)

from .parameters import delimiters, answer_line_prefixes
from .custom_operations import perform_solver_based_operation

def get_unique_output_filepaths(op_filepaths):
    unique_op_filepaths = set()
    instances = set()
    for op_filepath in op_filepaths:
        instance = "/".join(op_filepath.split("/")[1:-2])
        if instance in instances:
            continue
        unique_op_filepaths.add(op_filepath)
        instances.add(instance)

    return unique_op_filepaths
    
def save_constraints(solver: str, results_path: str, rel_instance_path: str) -> bool:
    """
    Writes answer sets and constraints to files
    """
    df = pd.read_csv(match_files[0])
    df = df[df[solver] == "SAT"]
    op_filepaths = df["instance"]
    op_filepaths = get_unique_output_filepaths(op_filepaths)

    for op_filepath in op_filepaths:
        filepath = "/".join(op_filepath.split("/")[1:-2])

        instance_path = get_instance_path(filepath, rel_instance_path)
        dest_path = get_destination_path("temp_instances", filepath)
        filename = copy_instance(instance_path, dest_path)

        path = os.path.join(
            os.getcwd(), 
            results_path, 
            op_filepath
        )
        
        answer_line_index = find_answer_line_index(solver, path)     
        answer_set = get_answer_set(path, answer_line_index)
        answer_set = remove_prefix(answer_set, solver)
        
        as_atoms = get_as_atoms(answer_set, delimiter=delimiters.get(solver))
        as_atoms = perform_solver_based_operation(solver, as_atoms)

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

def get_answer_set(path, line_index):
    with open(path, "r") as file:
        lines = file.readlines()
        
    answer_set = lines[line_index]
    return answer_set

def remove_prefix(answer_set, solver):
    if solver not in answer_line_prefixes:
        return answer_set
    prefix = answer_line_prefixes[solver]
    return answer_set.replace(prefix, "")
