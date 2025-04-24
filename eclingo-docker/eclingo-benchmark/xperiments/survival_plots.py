import argparse
import itertools
import math
import os
import pandas as pd
from pathlib import Path
from .ods_to_excel import OUTPUT_FOLDER, TIMEOUT_DURATION


pd.options.display.float_format = '{:,.1f}'.format

def create_tex_file(combined_df, solvers):
    """
    Generates tex file that will create cactus plot when compiled
    """
    
    times = {}
    for column in combined_df.columns[1:]:
        times[column] = list(combined_df[column])
    
    all_times = list(itertools.chain.from_iterable(times.values()))
    all_times.sort()
    
    max_time = float(math.ceil(max(all_times))) # Get which is the maximum time for running.
    max_time = min(max_time, TIMEOUT_DURATION)
    y_tick = {i*max_time/5 for i in range(1,6)}
    
    max_x = (math.ceil(len(all_times)/len(solvers)) + 1)
    x_tick = set(range(1, max_x, max(1, int(max_x/5))))
    

    tex= f'''
\\documentclass{{standalone}}

\\usepackage{{pgfplots}}

\\pgfplotsset{{compat = newest}}

\\begin{{document}}
\\begin{{tikzpicture}}
\\begin{{axis}}[
    title={{Survival Plot for Solvers}},
    ylabel={{Time(Seconds)}},
    xlabel={{#No of Instances solved}},
    ymin=0, ymax={max_time},
    xmin=0, xmax={max_x},
    ytick={str(y_tick)},
    xtick={str(x_tick)},
    legend pos=north west,
    ymajorgrids=true,
    grid style=dashed,
]
'''

    colors = ["red", "blue", "green", "yellow", "black"]
    while len(times) > len(colors):
        colors = colors + colors
    
    for j, t in enumerate(times):
        ti = times[t]
        ti.sort()
        coordinates = []
        for i in range(len(ti)):
            s = "(" + str(i+1) + "," +  str(ti[i]) + ")"
            coordinates.append(s)

        coordinates_str = ''.join(coordinates)

        tex += f'''
\\addplot[
color={colors[j]},
mark=*,
]
coordinates {{
{coordinates_str}
}};
\\addlegendentry{{ {solvers[j]} }}
        '''
        
    tex += f'''
\end{{axis}}
\end{{tikzpicture}}
\end{{document}}
    '''

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    write_path = os.path.join(OUTPUT_FOLDER, "results.tex")
    f = open(write_path, "w")
    f.write(tex)
    f.close()
    
    print("Tex file written at", write_path)

def get_ods_filepath(solver):
    """
    Returns absolute path of the output ods file for given solver
    """
    root_dir = Path(__file__).resolve().parent.parent
    relative_path = str(root_dir/"running"/f"benchmark-tool-{solver}"/"experiments"/"results"/f"{solver}"/f"{solver}.ods")
    return os.path.join(root_dir, relative_path)

    