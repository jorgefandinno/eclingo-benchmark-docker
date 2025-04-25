def remove_predicate_from_answer_set(answer_set_atoms, predicate):
    return [atom for atom in answer_set_atoms if predicate not in atom]

def clingo_dl_operations(answer_set_atoms):
    answer_set_atoms = remove_predicate_from_answer_set(answer_set_atoms, "dl")
    return answer_set_atoms

def perform_solver_based_operation(solver, answer_set_atoms):
    operation = custom_operations.get(solver)
    if not operation:
        return answer_set_atoms
    return operation(answer_set_atoms)

custom_operations = {
    "clingo-dl": clingo_dl_operations
}