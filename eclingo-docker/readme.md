
# How to build and run image from Dockerfile

**Clone repository and go to required directory:**
```
git clone <repository-url>
cd eclingo-benchmark-docker/eclingo-docker/
```

**Build docker image:**
```
# In directory with dockerfile
docker build -t <image-name:tag> .
docker build -t eclingo-benchmark .
```

**Save build logs to a log file:**
```
# --no-cache ignores cached layers
docker build -t <image-name:tag> --no-cache --progress=plain . &> build.log
docker build -t eclingo-benchmark --no-cache --progress=plain . &> build.log
```

**Run docker container:**
```
# -e is flag for overwriting environment variable
docker run [-e <variable-name>=<value>] <image-name:tag>
docker run eclingo-benchmark 

# -i for interactive, -t for terminal
docker run -it <image-name:tag> /bin/bash
docker run -it eclingo-benchmark /bin/bash
```

**Save container as image:**
```
docker commit <container-id> <new-image-name:tag>
docker commit cebe1c44fb02 eclingo-benchmark-new
```

# How to add new solver
```
# inside eclingo-docker/eclingo-benchmark/

- In run.sh file, add solver name in VALID_ARGS
- In run-benchmark.py 
    - add solver name in COMMANDS
    - add an elif statement for new solver in prepare_benchmarks() and use prepare_any_benchmarks() function in body
- In Dockerfile, update environment variables.
```

```
# inside eclingo-docker/eclingo-benchmark/output_operations/

- In parameters.py file, add parameters with respect to the solver outputs.
- Parameters:
    - answer_line_indices: line number of the answer set in the output
    - delimiters: what characters separate the atoms in the answer set (not required if whitespace)
    - answer_line_prefixes: what word precedes the answer set in the output
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
