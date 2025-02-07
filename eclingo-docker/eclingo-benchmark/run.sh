#!/bin/bash
current_dir=$(pwd)

# Epistemic Solver Possibilities 
# eclingo-old           -> Based on the environment used and the version installed, one could run the original version or the new version.
# eclingo               -> Run newer eclingo reification version without propagation of facts.
# ep_asp                -> Run EP-ASP solver.
# ep_asp_no_planning    -> Run EP-ASP solver without planning cues given by planning=0 parameter. "Vanilla version".
# selp                  -> Run selp solver.
# qasp                  -> Run elp2qasp solver.

# Define a list of valid arguments
VALID_ARGS=("eclingo-old" "eclingo" "ep_asp" "ep_asp_no_planning" "selp" "qasp" "ezsmt" "clingcon")

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "No argument provided. Please provide an argument."
  exit 1
fi

# check if the second argument is provided and is one of either benchmark or max-instances
additional_args=""
if [ -n "$2" ] && ([[ "$2" == "--benchmark="* ]] || [[ "$2" == "--max-instances="* ]]); then
  additional_args+="$2"
fi

# check for third argument and concat with second argument
if [ -n "$3" ] && ([[ "$3" == "--benchmark="* ]] || [[ "$3" == "--max-instances="* ]]); then
  additional_args+=" $3"
fi

# Check if the provided argument is in the list of valid arguments
if [[ " ${VALID_ARGS[@]} " =~ " $1 " ]]; then
  if [ -n "${additional_args}" ]; then
    # If valid, execute the Python script with all the provided argument
    python3 run-benchmark.py ${additional_args} $1
  else
    # execute the Python script with only solver name
    python3 run-benchmark.py $1
  fi
else
  # If not valid, print an error message
  echo "Error: '$1' is not a valid argument."
  echo "Valid arguments are: ${VALID_ARGS[@]}"
  exit 1
fi

# Process odf to xlsx for recreating paper plots
python3 xperiments/recreation_plots.py ${1}