import argparse
import os

import benchmark_runner

from prepare_benchmarks import (
    prepare_benchmarks_eclingo,
    prepare_benchmarks_ep_asp,
    prepare_benchmarks_selp,
    prepare_benchmarks_qasp,
    prepare_any_benchmarks,
)

IDLV = "idlv/idlv"

BENCHMARKS="./benchmarks"
BENCHMARK_TOOL="./benchmark-tool"

# Add command eclingo --ignore-shows --preprocessing-level=3 --no-eclingo-propagate --stats
COMMANDS = {"eclingo-old": f"eclingo $@\n\n",
            "eclingo": f"eclingo --ignore-shows --preprocessing-level=3 --no-eclingo-propagate --stats $@\n\n",
            "ep_asp":  f"bash \"$@\"\n\n",
            "ep_asp_no_planning":  f"bash \"$@\"\n\n",
            "selp":    f"bash \"$@\"\n\n",
            "qasp":    f"bash \"$@\"\n\n",
            "ezsmt": f"ezsmt -V 0 $@\n\n",
            "clingcon": f"clingcon $@\n\n",
            "clingo": f"clingo $@\n\n",
        }

SHOW_COMMAND_GROUNDERS = {"show-gringo", "show-idlv"}

COMMAND_GROUNDERS = COMMANDS.keys()

BENCHMARK_ORIGIN = {}

for command in COMMAND_GROUNDERS:
    BENCHMARK_ORIGIN[command] = BENCHMARKS
    
for command in SHOW_COMMAND_GROUNDERS:
    BENCHMARK_ORIGIN[command] = BENCHMARKS

parser = argparse.ArgumentParser(prog='Run grounder')
parser.add_argument("--benchmark", default="all")
parser.add_argument("--max-instances")
subparsers = parser.add_subparsers(title='subcommands', help='additional for help', dest="command")
subparsers.required = True

for command in COMMANDS:
    gringo_parser = subparsers.add_parser(command)
args = parser.parse_args()

command_splitted = args.command.split("-")
if len(command_splitted) > 1 and command_splitted[1] == "forget":
    command_splitted[1] = "pre-forget"
command_dir = "-".join(command_splitted)

# Mirror of benchmark execution for results
BENCHMARK_RUNNING=f"./running/benchmark-tool-{command_dir}"

def prepare_benchmarks():
    
    # Get specific benchmark origin based on solver used.
    benchmark_origin = BENCHMARK_ORIGIN[args.command]
    
    # Ensure that eclingo-old is redirected to eclingo benchmark folders, but uses extra commands
    benchmark_origin = os.path.join(benchmark_origin, command_dir)
    if benchmark_origin == "./benchmarks/eclingo-old":
        benchmark_origin = "./benchmarks/eclingo"
    
    print(f"benchmark origin: {benchmark_origin}, command dir: {command_dir}")
    benchmark = args.benchmark
    
    try:
        max_instances = int(args.max_instances) if args.max_instances is not None else None
    except ValueError:
        raise ValueError(f"The value for max_instances argument must be an integer !!")
   
    if command_dir == "eclingo" or command_dir == "eclingo-old":
        print(f"\nUsing solver: Eclingo")
        prepare_benchmarks_eclingo(benchmark, benchmark_origin, BENCHMARK_RUNNING, max_instances)
                
    elif command_dir == "ep_asp":
        print(f"\nUsing solver: EP-ASP")
        prepare_benchmarks_ep_asp(benchmark_origin, BENCHMARK_RUNNING)
                
    elif command_dir == "ep_asp_no_planning":
        print(f"\nUsing solver: EP-ASP No Planning")
        prepare_benchmarks_ep_asp(benchmark_origin, BENCHMARK_RUNNING)
                    
    elif command_dir == "selp":
        print(f"\nUsing solver: SELP")
        prepare_benchmarks_selp(benchmark_origin, BENCHMARK_RUNNING)
                    
    elif command_dir == "qasp":
        print(f"\nUsing solver: QASP")
        prepare_benchmarks_qasp(benchmark_origin, BENCHMARK_RUNNING)
    
    elif command_dir == "ezsmt" or command_dir == "clingcon" or command_dir == "clingo":
        benchmark_origin = "./benchmarks/clingo"
        print(f"\nUsing solver {command_dir}")
        prepare_any_benchmarks(benchmark, benchmark_origin, BENCHMARK_RUNNING, max_instances)
                
                
def grounder_solver(solver_file):
    solver_file.write("#!/bin/bash\n")
    solver_file.write("#\n")
    solver_file.write(COMMANDS[args.command])

# Declaring config file for instance and benchmark setup
config_file = "run-benchmark.xml"

br = benchmark_runner.BenchmarkRunner(prepare_benchmarks, BENCHMARK_RUNNING, grounder_solver, args.command, config_file)
br.do_benchmarks()