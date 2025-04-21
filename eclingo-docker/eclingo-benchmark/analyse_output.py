import argparse
from xperiments import (
    create_excel_sheets, 
    create_tex_file, 
    get_ods_filepath
)
from output_operations import match_files

def main(solvers, ods_file_paths):
    timed_out_file_path = match_files[2]
    
    combined_df, _ = create_excel_sheets(
        solvers, ods_file_paths, timed_out_file_path, print_results=False
    )
    
    create_tex_file(combined_df, solvers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--solvers", nargs='+', help="Name of solvers to use for plotting", required=True)
    # parser.add_argument("-t", "--time-out", help="Time out duration", default=600)
    
    args = parser.parse_args()._get_kwargs()
    solvers = args[0][1]
    
    ods_file_paths = [get_ods_filepath(solver) for solver in solvers]
    
    main(solvers, ods_file_paths)
    