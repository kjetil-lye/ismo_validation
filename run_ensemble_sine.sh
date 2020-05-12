#!/bin/bash
set -e
export PYTHONPATH=${PYTHONPATH}:$(pwd)/iterative_surrogate_optimization:$(pwd)
mkdir -p ensemble_output
cd ensemble_output
python -m ismo.bin.run_ensemble --script_name submit_sine.py --source_folder validation/examples/sine "$@"
