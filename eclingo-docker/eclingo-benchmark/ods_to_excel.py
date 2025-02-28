import ezodf
import os
import pandas as pd

from pathlib import Path


def get_ods_filepath(solver):
    root_dir = Path(__file__).resolve().parent
    relative_path = f"running/benchmark-tool-{solver}/experiments/results/{solver}/{solver}.ods"
    return os.path.join(root_dir, relative_path)

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

def load_ods_to_df(solver):
    filepath = get_ods_filepath(solver)
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

def get_combined_df(df_1, df_2):
    combined_df = pd.DataFrame()
    combined_df["instances"] = df_1["instances"]
    combined_df[f"{solver_1}"] = df_1[f"{solver_1}_average"]
    combined_df[f"{solver_2}"] = df_2[f"{solver_2}_average"]
    return combined_df

def get_aggregate_solver_times(combined_df):
    combined_df = combined_df.copy()
    combined_df["instances"] = [instance.split("/")[0] for instance in combined_df["instances"]]
    aggregate_df = combined_df.groupby("instances").mean()

    s1_df = combined_df[["instances", f"{solver_1}"]]
    s1_df = s1_df[s1_df[f"{solver_1}"] < 600]

    s2_df = combined_df[["instances", f"{solver_2}"]]
    s2_df = s2_df[s2_df[f"{solver_2}"] < 600]

    aggregate_df[f"{solver_1}_count"] = s1_df.groupby("instances")[f"{solver_1}"].count()
    aggregate_df[f"{solver_2}_count"] = s2_df.groupby("instances")[f"{solver_2}"].count()
    
    return aggregate_df

def main(solver_1, solver_2, print_results=True):
    df_1 = load_ods_to_df(solver_1)
    df_2 = load_ods_to_df(solver_2)
    
    combined_df = get_combined_df(df_1, df_2)
    combined_df.to_excel("combined.xlsx")
    if print_results:
        print(combined_df)
    
    aggregate_df = get_aggregate_solver_times(combined_df)
    aggregate_df.to_excel("aggregate.xlsx")
    if print_results:
        print(aggregate_df)


if __name__ == "__main__":
    solver_1 = "eclingo"
    solver_2 = "eclingo-old"
    main(solver_1, solver_2)