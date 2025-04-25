import argparse
from xperiments import (
    create_excel_sheets, 
    create_tex_file, 
    get_ods_filepath
)
from output_operations import match_files

def main(solvers, ods_file_paths, timeout_duration, benchmark_iteration):
    timed_out_file_path = match_files[2]
    
    combined_df, _ = create_excel_sheets(
        solvers, ods_file_paths, timed_out_file_path, timeout_duration, benchmark_iteration, print_results=False
    )
    
    create_tex_file(combined_df, solvers, timeout_duration)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--solvers", nargs='+', help="Name of solvers to use for plotting", required=True)
    parser.add_argument("-t", "--timeout", help="Time out duration", default=600)
    parser.add_argument("-i", "--iteration", help="Number of times, the benchmarks were repeated", default=2)
    
    args = parser.parse_args()
    solvers = args.solvers
    timeout_duration = float(args.timeout)
    benchmark_iteration = int(args.iteration)
    
    ods_file_paths = [get_ods_filepath(solver) for solver in solvers]
    
    main(solvers, ods_file_paths, timeout_duration, benchmark_iteration)
    