
# How to use the Benchmarking Platform
The following instructions require Docker to be installed and running.

### Clone repository and go to required directory:
```
git clone <repository-url>
cd eclingo-benchmark-docker/eclingo-docker/
```

### Run everything at once (if everything is setup)
Run the below command, if everything is already setup. <br>
**OR** <br>
Create a similar bash script if using new solvers. <br>
<br>
If running for the first time, consider checking [adding new solver](#how-to-add-new-solver) and [adding new benchmarks](#how-to-add-new-benchmarks-for-solvers). <br>
```
./compare.sh
```
[compare.sh](compare.sh) has three steps: [Building docker image](###Build-docker-image), [Running docker container](###Run-docker-container), and Copying results from container to host machine.

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

# How to add new solver

### Inside eclingo-docker/eclingo-benchmark/
```
- In run.sh file, add solver name in VALID_ARGS

- In run-benchmark.py 
    - add solver name in COMMANDS
    - add an elif statement for new solver in prepare_benchmarks() and use prepare_any_benchmarks() function in body
    - update benchmark_origin after [adding benchmarks](#How-to-add-new-benchmarks-for-solvers).

- In Dockerfile, update environment variables and setup bash script.
```

### Inside eclingo-docker/eclingo-benchmark/output_operations/
```
- In parameters.py file, add parameters with respect to the solver outputs.

- Parameters:
    - answer_line_indices: line number of the answer set in the output
    - delimiters: what characters separate the atoms in the answer set (not required if whitespace)
    - answer_line_prefixes: what word precedes the answer set in the output
    - relative_indices: Find line index of answer set with relative index of another word
```

### Update eclingo-docker/setup.sh.
If using new solvers, create a similar bash script as [setup.sh](setup.sh) or update the existing one.
```
- This contains all the operations that run inside the docker container.

- If not building docker image and running container, 
    - Create and/or activate the benchmarking environment.
    - Run the commands from setup.sh by replacing the variables for benchmarking and comparison.
```


# How to add new benchmarks for solvers
```
# inside eclingo-docker/eclingo-benchmark/benchmarks/

- Create a directory with solver name.
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
