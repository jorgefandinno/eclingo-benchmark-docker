#!/bin/bash

eval "$(conda shell.bash hook)"

conda activate ${env_name_1}
./run.sh ${solver_1} --max-instances=${max_instances} --benchmark=${benchmark}
conda activate ${env_name_2}
./run.sh ${solver_2_name} --max-instances=${max_instances} --benchmark=${benchmark}
python examine_output.py -s1 ${solver_1} -s2 ${solver_2} -s2n ${solver_2_name} > log.txt