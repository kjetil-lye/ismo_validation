#!/bin/bash
set -e
bash ../../../run_python_script.sh -m validation.bin.run_all_configurations submit_sine.py "$@"
