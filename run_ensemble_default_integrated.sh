#!/bin/bash
export OMP_NUM_THREADS=1

export PYTHONPATH=${PYTHONPATH}:$(pwd)/iterative_surrogate_optimization:$(pwd)
mkdir ensemble_output
cd ensemble_output
python ../ensemble_run/run_ensemble_integrated.py "$@"
