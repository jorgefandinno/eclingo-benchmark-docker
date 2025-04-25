#!/bin/bash

# initialize conda shell
eval "$(conda shell.bash hook)"

# Comparison between ezsmt and clingcon
conda activate ${env_name}
./run.sh ${solver_1} --max-instances=${max_instances} --benchmark=${benchmark}
./run.sh ${solver_2} --max-instances=${max_instances} --benchmark=${benchmark}
./run.sh ${solver_3} --max-instances=${max_instances} --benchmark=${benchmark}
./run.sh ${solver_4} --max-instances=${max_instances} --benchmark=${benchmark}

# check if output from solvers are consistent against each other
python examine_output.py -s1 ${solver_1} -s2 ${solver_2} > log.txt
python examine_output.py -s1 ${solver_1} -s2 ${solver_3} >> log.txt
python examine_output.py -s1 ${solver_1} -s2 ${solver_4} >> log.txt

# create comparison excel sheets and graphs
python analyse_output.py -s ${solver_1} ${solver_2} ${solver_3} ${solver_4} -t 30 >> log.txt