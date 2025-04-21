#!/bin/bash

# initialize conda shell
eval "$(conda shell.bash hook)"

# Comparison between eclingo-new and eclingo-old
conda activate ${env_name_1}
./run.sh ${solver_1_name} --max-instances=${max_instances} --benchmark=${benchmark}
conda activate ${env_name_2}
./run.sh ${solver_2_name} --max-instances=${max_instances} --benchmark=${benchmark}

# check if output from solvers are consistent against each other
python examine_output.py -s1 ${solver_1} -s2 ${solver_2} -s2n ${solver_2_name} > log.txt

# create comparison excel sheets and graphs
python analyse_output.py -s ${solver_1_name} ${solver_2_name} >> log.txt

