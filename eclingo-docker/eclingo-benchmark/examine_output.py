import argparse

from output_operations import (
    check_output_satisfiability, 
    save_constraints, 
    check_output_consistency
)

def main(solvers, line_number):
    (s1_name, solver_1), (s2_name, solver_2) = solvers

    s1_results_path = f"running/benchmark-tool-{s1_name}/output/project/zuse/results/suite/"
    s2_results_path = f"running/benchmark-tool-{s2_name}/output/project/zuse/results/suite/"

    check_output_satisfiability(s1_name, s2_name, s1_results_path, s2_results_path)

    rel_instance_path = f"running/benchmark-tool-{s1_name}/experiments/instances"
    save_constraints(s1_name, s1_results_path, rel_instance_path, line_number)

    check_output_consistency(s2_name, solver_2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s1", "--solver-1", required=True, help="solver 1 name used in commands")
    parser.add_argument("-s1n", "--solver-1-name", help="name used to save solver 1 results if different than the original name; defaults to solver 1 name if not provided")
    parser.add_argument("-s2", "--solver-2", required=True, help="solver 2 name used in commands")
    parser.add_argument("-s2n", "--solver-2-name", help="name used to save solver 2 results if different than the original name; defaults to solver 2 name if not provided")
    parser.add_argument("-l", "--line-number", help="line number where the answer set is located in solver file after benchmark is executed")

    args = parser.parse_args()

    solver_1 = args.solver_1
    if args.solver_1_name:
        s1_name = args.solver_1_name
    else:
        s1_name = solver_1

    solver_2 = args.solver_2
    if args.solver_2_name:
        s2_name = args.solver_2_name
    else:
        s2_name = solver_2

    line_number = int(args.line_number)

    solvers = (
        (s1_name, solver_1),
        (s2_name, solver_2),
    )

    main(solvers, line_number)
