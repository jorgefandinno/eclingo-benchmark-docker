import ezodf
import os
import pandas as pd
from pathlib import Path

TIMEOUT_DURATION = 600
BENCHMARK_ITERATION = 2

OUTPUT_FOLDER = os.path.join(
    str(Path(__file__).resolve().parent.parent),
    "analysis"
)

def filter_df(df):
    df = df.drop(columns = ["min", "median", "max"])
    df = df.dropna(axis = 1, how = 'all')
    
    keywords = ["SUM", "AVG", "DEV", "DST", "BEST", "BETTER", "WORSE", "WORST"]
    # create a boolean mask identifying rows with keywords
    mask = df["instance"].str.contains('|'.join(keywords), case=False, na=False)
    df = df[~mask]
    
    df = df.dropna(axis=0)
    return df

def update_memory_error_instances(df, timed_out_file_path):
    root_dir = Path(__file__).resolve().parent.parent
    path = str(root_dir/timed_out_file_path)
    if not os.path.exists(path):
        return df
    
    timed_out_df = pd.read_csv(path)
    timed_out_df["instance"] = list(
        map(
            lambda x: os.path.join(*x.split("/")[1:-2]), 
            timed_out_df["instance"].tolist()
        )
    )
    
    columns = timed_out_df.columns
    solver_count = len(columns) - 1
    
    for row in timed_out_df.itertuples():
        instance = row[1]
        for i in range(0, solver_count-1):
            solver = columns[i+1]
            if row[i+2] == "None":
                mask = (df["instance"] == instance)
                df.loc[mask, solver] = TIMEOUT_DURATION
    return df

def update_timed_out_instances(df, solver):
    for idx in range(1, BENCHMARK_ITERATION+1):
        df[f"{solver}_{idx}"] = [value if value <= TIMEOUT_DURATION else TIMEOUT_DURATION for value in df[f"{solver}_{idx}"]]
    return df

def load_ods_to_df(filepath, solver):
    spreadsheet = ezodf.opendoc(filepath)
    sheet = spreadsheet.sheets[0]  # access the first sheet

    all_values = []
    for row in sheet.rows():
        row_list = []
        for cell in row:
            row_list.append(cell.value)
        all_values.append(row_list)
        
    columns = all_values[0]
    columns[0] = "instance"
    solver_columns = [f"{solver}_{idx}" for idx in range(1, BENCHMARK_ITERATION+1)]
    columns[1:BENCHMARK_ITERATION+1] = solver_columns
    
    all_values = all_values[2:]

    df = pd.DataFrame(all_values, columns=columns)
    df = filter_df(df)
    df = update_timed_out_instances(df, solver)
    
    sum_all_iterations = sum(df[column] for column in solver_columns)    
    df[f"{solver}_average"] = sum_all_iterations/BENCHMARK_ITERATION

    return df

def get_combined_df(dfs, solvers):
    combined_df = pd.DataFrame()
    combined_df["instance"] = dfs[0]["instance"]
    for i, solver in enumerate(solvers):
        combined_df[solver] = dfs[i][f"{solver}_average"]
    return combined_df

def get_aggregate_solver_times(combined_df, solvers):
    combined_df = combined_df.copy()
    combined_df["instance"] = [instance.split("/")[0] for instance in combined_df["instance"]]
    aggregate_df = combined_df.groupby("instance").mean()

    for solver in solvers:
        df = combined_df[["instance", solver]]
        df = df[df[solver] < TIMEOUT_DURATION]
        aggregate_df[f"{solver}_count"] = df.groupby("instance")[solver].count()
    
    return aggregate_df

def create_excel_sheets(solvers, file_paths, timed_out_file_path, print_results=True):
    """
    Create excels sheets from ods files
    combined.xlsx with average time for all instances of a benchmark
    aggregate.xlsx with average time for each benchmark
    """
    
    dfs = []
    for i, solver in enumerate(solvers):
        df = load_ods_to_df(file_paths[i], solver)
        dfs.append(df)
        
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    combined_df = get_combined_df(dfs, solvers)
    combined_df = update_memory_error_instances(combined_df, timed_out_file_path)
    file_name = os.path.join(OUTPUT_FOLDER, "combined.xlsx")
    combined_df.to_excel(file_name, index=False)
    print("Average benchmark times for all instances of all benchmarks saved in", file_name)
    
    if print_results:
        print(combined_df)

    aggregate_df = get_aggregate_solver_times(combined_df, solvers)
    file_name = os.path.join(OUTPUT_FOLDER, "aggregate.xlsx")
    aggregate_df.to_excel(file_name)
    print("Average benchmark times and count for each benchmark saved in", file_name)
    
    if print_results:
        print(aggregate_df)
        
    return combined_df, aggregate_df
