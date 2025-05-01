# Reproducible Benchmarking Platform
The Benchmarking Platfrom is used to compare Answer Set Programming (ASP)
solvers by running benchmark programs and comparing their outputs against each other. 
The platform builds on top of a benchmarking tool that evaluates a solver's performance
and enables users to compare performances of multiple solvers or even two
different versions of the same solver. The output of one of the solvers 
is used to create a constraint program, which, along with the original program, 
is then passed on to the second solver to ensure that the results are consistent. 
Similarly, the outputs are used to analyze the solvers' performance by generating 
spreadsheets and graphs. The entire process is automated through the 
use of Docker containers. This way, the platform avoids the time-consuming 
process of manually preparing benchmarking environments before each benchmark run, 
making the whole process easily reproducible as well.

Please see the attached [presentation slides](Reproducible-benchmarking-platform.pptx) for more information.

# How to use the Benchmarking Platform
The following instructions require Docker to be installed and running.

## Clone repository and go to required directory:
```
git clone <repository-url>
cd eclingo-benchmark-docker/
```

## Bash Script for Docker Instructions

If running for the first time, consider comparing between two versions of eclingo as described in the following section. <br>
Currently, the platform supports these solvers: eclingo, ezsmt, clingcon, clingo, clingo-dl. 


If adding a new solver, one may have to update some scripts such as [examine_output.py](run-benchmark/examine_output.py). More details can be found in these sections: [adding new solver or updating existing configuration](#how-to-add-new-solver-or-update-existing-configuration)
and [adding new benchmarks](#how-to-add-new-benchmarks). <br>

If required comparison script exists for the solvers, run the comparison script. See below for more examples on comparison script. 
More details on how to create a new comparison script can be found in [Create/Update compare.sh](#createupdate-comparesh) section.

### Comparison Script for Eclingo Comparison
If benchmarking and comparing two different eclingo versions, run the [compare.sh](compare.sh) bash script.
```
./compare.sh
```

[compare.sh](compare.sh) has three steps: 
1. [Building docker image](#build-docker-image)
2. [Running docker container](#run-docker-container)
3. Copying results from container to host machine. <br>

#### [Building docker image](#build-docker-image)
[Building docker image](#build-docker-image) requires [Dockerfile](Dockerfile) that contains instructions for installation and preparing benchmarking platform. 
This also copies [setup.sh](setup.sh) file to the image, which is the entrypoint while running the container.

#### [Running docker container](#run-docker-container)
Running docker container involves running [setup.sh](setup.sh) bash script inside the container. 
Environment variables from [Dockerfile](Dockerfile) can be updated at runtime as shown [here](#run-docker-container).

[setup.sh](setup.sh) has three steps:

1. [Running benchmark](run-benchmark/run.sh)

```
./run.sh ${solver} --benchmark=${benchmark} --max-instances=${max_instances} 
```

This uses the benchmarking tool to run the benchmark problems. The configuration 
for the benchmarking operation such as timeout duration and memory can be set up 
in [run-benchmark.xml](run-benchmark/run-benchmark.xml). The environment variables such as "benchmark" and 
"max-instances" can be updated at runtime using -e flag as explained under the "Running docker container" section above.
Please see [updating existing configuration](#how-to-add-new-solver-or-update-existing-configuration) 
for updating more configurations.

2. [Comparing Output](run-benchmark/examine_output.py)

This script compares the output of the benchmark problems for two different solvers.
This checks satisfiability for each instance and consistency among solvers. It 
also compares the output by creating constraints from the output of the first solver and
passing it to the second solver along with original program.
```
python examine_output.py -s1 ${solver_1} -s2 ${solver_2} -t 600
```
```
Arguments:
    -s1 -> solver 1
    -s2 -> solver 2
    -t -> timeout duration for second solver (seconds)
```
If any of the solvers above is not supported, you have to update the "examine_output.py" script accordingly.


3. [Analyse Output](run-benchmark/analyse_output.py)

This script analyses the output of the benchmark problems for multiple solvers.
It compares the solver performances side by side and also aggregates performances 
by creating two different excel sheets. A survival/cactus plot is also generated 
using the generated excel sheet.
```
python analyse_output.py -s ${solver_1} ${solver_2} -t 600 -i 2
```
```
Arguments:
    -s -> solvers
    -t -> timeout duration to calculate solved instances (seconds)
    -i -> number of iterations of running benchmarks
```

#### Copying results from container to host machine
The process when completed stores all the results in the docker container. The results are copied back to the host machine using docker copy commands. The results are stored in the directory "results" of the host machine.


Now, we list the remaining comparison scripts for comparing supported solvers.

### Comparison Script for EZSMT and Clingo-dl Comparison
If benchmarking and comparing ezsmt with clingcon, run the [compare-ezsmt-clingcon.sh](compare-ezsmt-clingcon.sh) bash script. <br>
```
./compare-ezsmt-clingcon.sh
```

### Comparison Script for EZSMT and Clingcon Comparison
If benchmarking and comparing clingo-dl with three different IDL versions of EZSMT, run the [compare-ezsmt-clingodl.sh](compare-ezsmt-clingodl.sh) bash script. <br>
```
./compare-ezsmt-clingodl.sh
```


# How to add new solver or update existing configuration

If you are adding a new solver, begin by creating a new directory within eclingo-benchmark-docker and prepare a Dockerfile inside.
<br>
For example: to compare a new solver ezsmt-z3 with clingcon, create a directory named "ezsmt-z3-clingcon-comparison". 

Copy a suitable Dockerfile, for example: ezsmt-clingcon-comparison/Dockerfile, into the created directory.<br>
There are some pre-prepared Dockerfiles related to the supported solvers within the repository, please choose a suitable one for your task and edit on top of that.

Make a copy of setup.sh file. <br>
For example: for ezsmt-z3 and clingcon comparison, copy setup-ezsmt-clingcon.sh file to setup-ezsmt-z3-clingcon.sh and modify it, if necessary.

See [Create/Update setup.sh](#createupdate-setupsh) section for more details on what "setup.sh" script does.

Now, modify the Dockerfile.
```
In Dockerfile:

- Update name of bash script to "setup-ezsmt-z3-clingcon-comparison.sh" in COPY command and CMD command.

- Update environment variables such as solver names, benchmarks, max_instances, and argument variable such as conda environment yml file.
    For environment yml file: Go to directory "run-benchmark/envs/". Make a copy of environment_ezsmt.yml and update it as required.
```
<br>
Modify the supporting scripts as follows:

### Inside run-benchmark/
```
- In run.sh file, add/update solver name in VALID_ARGS
    For example: "ezsmt-z3"

- In run-benchmark.py 
    - add/update solver name and a command for running the solver for an instance in COMMANDS. 
        For example: for using ezsmt-z3: {"ezsmt-z3": "ezsmt -V 0 -s z3 $@\n\n"}

    - add/update an elif statement for new solver in prepare_benchmarks() and use prepare_any_benchmarks() function in body
        For example: 
            elif command_dir == "ezsmt-z3":
                benchmark_origin = "./benchmarks/ezsmt"
                print(f"\nUsing solver {command_dir}")
                prepare_any_benchmarks(benchmark, benchmark_origin, BENCHMARK_RUNNING, max_instances)

    - update benchmark_origin after adding new benchmarks or by using existing benchmarks as shown above. Check how to add benchmarks below.

- In run-benchmark.xml, update timeout, memory, and other configuration for benchmarking if required.
```

### Inside run-benchmark/output_operations/
```
- In parameters.py file, add/update parameters with respect to the solver and solver outputs.

- Parameters:
    - solver_commands: Maps solver name to solver command as used before.
        For example: 
            for adding ezsmt-z3: 
                "ezsmt-z3": "ezsmt -V 0 -s z3"
            If not used in this mapping, solver command will be the same as the solver name provided.
    
    - answer_line_indices: Line number of the answer set for a solver in the solver output.

    - delimiters: What characters separate the atoms in the answer set? (not required if whitespace)
    
    - answer_line_prefixes: What word precedes the answer set in the solver output? The word will be filtered out.
    
    - relative_indices: Finds line index of the answer set for a solver with relative index of another word. 
                        This will be ignored if the solver has an entry in "answer_line_indices".
        For example: 
            for adding relative index for ezsmt-z3:
                "ezsmt-z3": ("SAT", 1)
            This tells the script to look for "SAT" keyword and add 1 to its index for answer line index.

- If adding a new solver that requires a custom parser, add custom parsing function in custom_operations.py
    For example:
        To add custom operation for clingo-dl solver, define a custom function "clingo_dl_operations" with 
        operations required for clingo-dl answer set parsing, and add it to the custom_operations dictionary.
            "clingo-dl": clingo_dl_operations

- If there are any errors while comparing the output, please look at the results files 
    and make necessary changes in the "parameters.py" file as required by the solver outputs.
    For example: updating solver command, updating answer line index, updating relative index, etc. 
```

### Create/Update setup.sh.
If using new solvers or updating existing ones, create a similar bash script as 
[setup.sh](setup.sh) or update the existing script.
```
- This contains all the operations that run inside the docker container.
    - Run Benchmarks
    - Compare Output
    - Analyse Output

- If running locally in the host machine without using docker container, 
    - Create and/or activate the benchmarking environment.
    - Run the commands from setup.sh by replacing the variables for benchmarking and comparison.
```

### Create/Update compare.sh

Once everything is done, create a new bash script to compare solvers.


For example: to compare ezsmt-z3 and clingcon, create a bash script named "compare-ezsmt-z3-clingcon.sh" 
by copying "compare-ezsmt-clingcon.sh" and changing the solver name variables, image name variable, 
and dockerfile location within the build command if required.

Now, after everything is done, run the compare bash script for ezsmt-z3 and clingcon comparison as follows:
```
./compare-ezsmt-z3-clingcon.sh
```


# How to add new benchmarks
```
# inside run-benchmark/benchmarks/

- Create a directory with a distinct name, e.g. solver_name.
- Copy benchmarks inside the created directory.
- The directory structure should be:

<solver_name>
|- <benchmark_1>
|   |- encodings
|   |   |- <encoding_1.lp>
|   |   |- <encoding_2.lp>
|   |- instances
|   |   |- <instance_1.lp>
|   |   |- <instance_2.lp>
|- <benchmark_2>
|   |- encodings
|   |   |- <encoding_1.lp>
|   |   |- <encoding_2.lp>
|   |- instances
|   |   |- <instance_1.lp>
|   |   |- <instance_2.lp>
```

# Docker Operations

### Build docker image
```
# In directory with dockerfile
docker build -t <image-name:tag> .
docker build -t eclingo-benchmark .
```

### Build docker image and save build logs to a log file
```
# --no-cache ignores cached layers
docker build -t <image-name:tag> --no-cache --progress=plain . &> build.log
docker build -t eclingo-benchmark --no-cache --progress=plain . &> build.log
```

### Run docker container
```
# -e is flag for overwriting environment variable
docker run [-e <variable-name>=<value>] <image-name:tag>
docker run eclingo-benchmark 

# -i for interactive, -t for terminal
docker run -it <image-name:tag> /bin/bash
docker run -it eclingo-benchmark /bin/bash
```

### Save container as image
```
docker commit <container-id> <new-image-name:tag>
docker commit cebe1c44fb02 eclingo-benchmark-new
```
