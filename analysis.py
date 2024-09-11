from cProfile import label
from optparse import Values
import os
import pandas as pd
import numpy as np
from IPython.display import display, HTML, Markdown, display_jpeg
import re
import math
from pathlib import Path
import itertools


def eclingo_instance_name(instance):
    name = Path(instance).stem.replace('eligible_eligible', 'eligible').replace('yale_yale', 'yale').replace('yale-parameter_yale', 'eiter_yale')
    if name.startswith('eligible') and "-" in name:
        name = name.split("-")[0]
    return name

def ep_asp_instance_name(instance):
    instance = Path(instance).stem
    parts = instance.split('_')
    if len(parts) > 1 and parts[1] == 'bomb':
        number = parts[2]
        if len(number) == 3:
            number = "0" + number
        if len(number) == 2:
            number = "00" + number
        name = f"{parts[0]}_bomb_{number}"
        if len(parts) > 3:
            name += f"_{parts[3]}"
        return name
    if instance.startswith('yale'):
        number = instance[len('yale'):]
        return f"yale0{number}"
    if instance.startswith('eiter_yale'):
        number = instance[len('eiter_yale'):]
        return f"eiter_yale0{number}"
    return instance

def selp_instance_name(instance):
    instance = Path(instance).stem.replace('newEligible', 'eligible')
    parts = instance.split('_')
    if len(parts) > 1 and parts[1] == 'bomb':
        number = parts[2]
        if len(number) == 3:
            number = "0" + number
        if len(number) > 4:
            number = number[-4:]
        name = f"{parts[0]}_bomb_{number}"
        if len(parts) > 3:
            name += f"_{parts[3]}"
        return name
    if instance.startswith('yale'):
        number = int(instance[len('yale'):])
        if number <= 8:
            return f"yale{number:02d}"
        if number <= 11:
            return f"eiter_yale{number-8:02d}"
        if number <= 14:
            return f"eiter_yale{number-9:02d}"
        return f"eiter_yale{number-8:02d}"
    return instance

def qasp_instance_name(instance):
    instance = Path(instance.replace('.lp.sh', '.lp')).stem.replace('newEligible', 'eligible').replace('eligible_qasp', 'eligible')
    if instance.startswith('eligible') and "-" in instance:
        return instance.split("-")[0].replace('_','')
    parts = instance.split('_')
    if len(parts) > 1 and parts[1] == 'bomb':
        number = parts[2]
        if len(number) == 3:
            number = "0" + number
        if len(number) > 4:
            number = number[-4:]
        name = f"{parts[0]}_bomb_{number}"
        if len(parts) > 3:
            name += f"_{parts[3]}"
        return name
    if instance.startswith('yale_'):
        number = int(instance[len('yale_'):])
        if number <= 8:
            return f"yale{number:02d}"
        if number <= 11:
            return f"eiter_yale{number-8:02d}"
        if number <= 14:
            return f"eiter_yale{number-9:02d}"
        return f"eiter_yale{number-8:02d}"
    return instance

dnamemap = {
    'eclingo-old' : eclingo_instance_name,
    'ep-asp'      : ep_asp_instance_name,
    'ep-asp-np'   : ep_asp_instance_name,
    'selp'        : selp_instance_name,
    'qasp'        : qasp_instance_name,
}

def read_xlsx(dfiles):
    dsolvers = dict()
    for solver, file in dfiles.items():
        dataFrame =  pd.read_excel(file)
        dataFrame.columns.values[0] = "instance"
        # print(dataFrame)
        last_row = dataFrame['median'].isnull().idxmax()
        if last_row == 0:
            last_row = len(dataFrame)
        # print(dataFrame[['instance', 'median']])
        # print(dataFrame[['instance', 'median']][1:last_row])
        dsolvers[solver] = dataFrame[['instance', 'median']][1:last_row]
        # print(dsolvers[solver])
        dsolvers[solver].sort_values(by='instance', inplace=True)
        
    column_names = ['instance', 'eclingo-pro'] + [s for s in dsolvers.keys() if s != 'eclingo-pro']
    newDataFrame = pd.DataFrame(columns= column_names)
    
    eclingo_pro_df = dsolvers['eclingo-pro']
    for row in eclingo_pro_df.iterrows():
        instance = row[1]['instance']
        instance = eclingo_instance_name(instance)
        eclingo_pro_time = row[1]['median']
        newRow = {'instance': instance, 'eclingo-pro': eclingo_pro_time}
        newDataFrame = newDataFrame._append(newRow, ignore_index=True)
    for solver, df in dsolvers.items():
        # print(solver)
        if solver == 'eclingo-pro':
            continue
        # if solver == 'ep-asp-np':
        #     print(df)
        for row in df.iterrows():
            instance = row[1]['instance']
            # if solver == 'qasp':
            #     print("------------", solver, instance)
            instance = dnamemap[solver](instance)
            time = row[1]['median']
            try:
                new_row = newDataFrame.loc[newDataFrame['instance'] == instance].index[0]
            except IndexError as e:
                print("-------- solver:", solver, "instance:", instance, "time:", time, "row[1]['instance']", row[1]['instance'])
                print("--------", newDataFrame.loc[newDataFrame['instance'] == instance])
                print(df)
                print("----------------")
                print(newDataFrame)
                raise e
            newDataFrame.at[new_row, solver] = time
    asswertion_sum = newDataFrame.isnull().sum().sum()
    assert asswertion_sum == 0, f"{asswertion_sum}\n{newDataFrame}"
    return newDataFrame

def different_instances(df, solver1, solver2, show_solver1=False, show_solver2=False):
    df1 = df[(df[solver1] < 600)  & (df[solver2] >= 600)]
    df2 = df[(df[solver1] >= 600) & (df[solver2] < 600)]
    if show_solver1 and len(df1) > 0:
        print(f"Instances solved by {solver1} and not by {solver2}")
        print(df1)
    if show_solver2 and len(df2) > 0:
        print(f"Instances solved by {solver2} and not by {solver1}")
        print(df2)
    return len(df1), len(df2)

def speed_up(df, solver1, solver2):
    sums = df.sum()
    raw_speed_up = sums[solver2] / sums[solver1]
    or_df = df[(df[solver1] < 600) | (df[solver2] < 600)]
    or_sums = or_df.sum()
    or_speed_up = or_sums[solver2] / or_sums[solver1]
    and_df = df[(df[solver1] < 600) & (df[solver2] < 600)]
    and_sums = and_df.sum()
    and_speed_up = and_sums[solver2] / and_sums[solver1]
    all_or_df = df[(df['eclingo-pro'] < 600) | (df['eclingo-old'] < 600) | (df['ep-asp'] < 600)]
    all_or_sums = all_or_df.sum()
    all_or_speed_up = all_or_sums[solver2] / all_or_sums[solver1]
    return {
        'raw_speed_up': raw_speed_up,
        'or_speed_up': or_speed_up,
        'and_speed_up': and_speed_up,
        'all_or_speed_up': all_or_speed_up,
        'or_count' : len(or_df),
        'and_count' : len(and_df),
        'all_or_count' : len(all_or_df),
    }

dfiles = {
    'eclingo-pro'  : 'eclingo_reif_YBE_Propagate_600s.xlsx',
    'eclingo-old'  : 'eclingo_YBE_600s.xlsx',
    'ep-asp'       : 'EP_ASP_YBE_600s.xlsx',
    'ep-asp-np'    : 'EP_ASP_NP_YBE_600s.xlsx',
    'selp'         : 'selp_YBE_600s.xlsx',
    'qasp'         : 'qasp_YBE_600s.xlsx',
}

dfiles = {k: Path(v) for k, v in dfiles.items()}

df = read_xlsx(dfiles)
# mask = df.apply(lambda x: x['instance'].startswith('eligible'), axis=1)
# mask = df.apply(lambda x: "bomb" in x['instance'], axis=1)
# df = df[mask]


print(f"Numeber of instances: {len(df)}")
solver1 = 'eclingo-pro'
solver2 = 'eclingo-old'
print(df)
print(f"Speed-ups {solver1} / {solver2}")
s = speed_up(df, solver1, solver2)
instances_sovler1, instances_solver2 =  different_instances(df, solver1, solver2)
print(f"Diffent instances. {solver1} =", instances_sovler1, f"{solver2} =", instances_solver2)
print(s)
print()
solver2 = 'ep-asp'
print(f"Speed-ups {solver1} / {solver2}")
instances_sovler1, instances_solver2 =  different_instances(df, solver1, solver2, show_solver2=True)
print(f"Diffent instances. {solver1} =", instances_sovler1, f"{solver2} =", instances_solver2)
s = speed_up(df, solver1, solver2)
different_instances(df, solver1, solver2)
print(s)
print()
solver2 = 'ep-asp-np'
print(f"Speed-ups {solver1} / {solver2}")
instances_sovler1, instances_solver2 =  different_instances(df, solver1, solver2, show_solver2=True)
print(f"Diffent instances. {solver1} =", instances_sovler1, f"{solver2} =", instances_solver2)
s = speed_up(df, solver1, solver2)
different_instances(df, solver1, solver2)
print(s)
print()
solver2 = 'selp'
print(f"Speed-ups {solver1} / {solver2}")
instances_sovler1, instances_solver2 =  different_instances(df, solver1, solver2)
print(f"Diffent instances. {solver1} =", instances_sovler1, f"{solver2} =", instances_solver2)
s = speed_up(df, solver1, solver2)
different_instances(df, solver1, solver2)
print(s)
print()
solver2 = 'qasp'
print(f"Speed-ups {solver1} / {solver2}")
instances_sovler1, instances_solver2 =  different_instances(df, solver1, solver2)
print(f"Diffent instances. {solver1} =", instances_sovler1, f"{solver2} =", instances_solver2)
s = speed_up(df, solver1, solver2)
different_instances(df, solver1, solver2)
print(s)
print()
