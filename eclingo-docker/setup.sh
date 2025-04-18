#!/bin/bash

# initialize conda shell
eval "$(conda shell.bash hook)"

# Comparison between eclingo-new and eclingo-old
conda activate ${env_name_1}
./run.sh ${solver_1} --max-instances=${max_instances} --benchmark=${benchmark}

conda activate ${env_name_2}
./run.sh ${solver_2_name} --max-instances=${max_instances} --benchmark=${benchmark}

python examine_output.py -s1 ${solver_1} -s2 ${solver_2} -s2n ${solver_2_name} > log.txt

python analyse.py -s ${solver_1_name} ${solver_2_name} >> log.txt


# # Comparison between ezsmt, clingcon and clingo
# conda activate ${env_name}
# ./run.sh ${solver_1} --max-instances=${max_instances} --benchmark=${benchmark}
# ./run.sh ${solver_2} --max-instances=${max_instances} --benchmark=${benchmark}
# ./run.sh ${solver_3} --max-instances=${max_instances} --benchmark=${benchmark}

# python examine_output.py -s1 ${solver_1} -s1n ${solver_1_name} -s2 ${solver_2} -s2n ${solver_2_name} > log.txt
# python examine_output.py -s1 ${solver_1} -s1n ${solver_1_name} -s2 ${solver_3} -s2n ${solver_3_name} >> log.txt

# python analyse.py -s ${solver_1_name} ${solver_2_name} ${solver_3_name} >> log.txt
