#!/bin/bash

# initialize conda shell
eval "$(conda shell.bash hook)"

# Comparison between ezsmt, clingcon and clingo
conda activate ${env_name}
./run.sh ${solver_1_name} --max-instances=${max_instances} --benchmark=${benchmark}
./run.sh ${solver_2_name} --max-instances=${max_instances} --benchmark=${benchmark}
./run.sh ${solver_3_name} --max-instances=${max_instances} --benchmark=${benchmark}

# check if output from solvers are consistent against each other
python examine_output.py -s1 ${solver_1} -s1n ${solver_1_name} -s2 ${solver_2} -s2n ${solver_2_name} > log.txt
python examine_output.py -s1 ${solver_1} -s1n ${solver_1_name} -s2 ${solver_3} -s2n ${solver_3_name} >> log.txt

# create comparison excel sheets and graphs
python analyse_output.py -s ${solver_1_name} ${solver_2_name} ${solver_3_name} >> log.txt