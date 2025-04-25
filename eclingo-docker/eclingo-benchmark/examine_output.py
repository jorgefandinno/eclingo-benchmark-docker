import argparse

from output_operations import (
    check_output_satisfiability, 
    save_constraints, 
    check_output_consistency
)

def main(solver_1, solver_2, timeout_duration):
    s1_results_path = f"running/benchmark-tool-{solver_1}/output/project/zuse/results/suite/"
    s2_results_path = f"running/benchmark-tool-{solver_2}/output/project/zuse/results/suite/"

    # check if SAT and UNSAT are consistent across both solvers
    check_output_satisfiability(solver_1, solver_2, s1_results_path, s2_results_path)

    # prepare constraints from answer sets of first solver
    rel_instance_path = f"running/benchmark-tool-{solver_1}/experiments/instances"
    save_constraints(solver_1, s1_results_path, rel_instance_path)

    # use constraints from first solver and check with second solver
    check_output_consistency(solver_2, timeout_duration)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s1", "--solver-1", required=True, help="solver 1 name used in commands")
    parser.add_argument("-s2", "--solver-2", required=True, help="solver 2 name used in commands")
    parser.add_argument("-t", "--timeout", default=610, help="Timeout duration for second solver while checking")

    args = parser.parse_args()
    solver_1 = args.solver_1
    solver_2 = args.solver_2
    timeout_duration = args.timeout

    main(solver_1, solver_2, timeout_duration)
