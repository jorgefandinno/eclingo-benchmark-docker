import ezodf
import os
import pandas as pd
from pathlib import Path

OUTPUT_FOLDER = os.path.join(
    str(Path(__file__).resolve().parent.parent),
    "analysis"
)

def filter_df(df):
    df = df.drop(columns = ["min", "median", "max"])
    df = df.dropna(axis = 1, how = 'all')
    
    keywords = ["SUM", "AVG", "DEV", "DST", "BEST", "BETTER", "WORSE", "WORST"]
    # create a boolean mask identifying rows with keywords
    mask = df["instances"].str.contains('|'.join(keywords), case=False, na=False)
    df = df[~mask]
    
    df = df.dropna(axis=0)
    return df

def update_timed_out_instances(df, solver):
    df[f"{solver}_1"] = [value if value <= 600 else 600 for value in df[f"{solver}_1"]]
    df[f"{solver}_2"] = [value if value <= 600 else 600 for value in df[f"{solver}_2"]]
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
    columns[:3] = ["instances", f"{solver}_1", f"{solver}_2"]
    all_values = all_values[2:]

    df = pd.DataFrame(all_values, columns=columns)
    df = filter_df(df)
    df = update_timed_out_instances(df, solver)
    df[f"{solver}_average"] = (df[f"{solver}_1"] + df[f"{solver}_2"])/2
    
    return df

def get_combined_df(dfs, solvers):
    combined_df = pd.DataFrame()
    combined_df["instances"] = dfs[0]["instances"]
    for i, solver in enumerate(solvers):
        combined_df[solver] = dfs[i][f"{solver}_average"]
    return combined_df

def get_aggregate_solver_times(combined_df, solvers):
    combined_df = combined_df.copy()
    combined_df["instances"] = [instance.split("/")[0] for instance in combined_df["instances"]]
    aggregate_df = combined_df.groupby("instances").mean()

    for solver in solvers:
        df = combined_df[["instances", solver]]
        df = df[df[solver] < 600]
        aggregate_df[f"{solver}_count"] = df.groupby("instances")[solver].count()
    
    return aggregate_df

def create_excel_sheets(solvers, file_paths, print_results=True):
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
