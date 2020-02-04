"""
Runs all configurations for analysis
"""

import sys
import os
import subprocess
import ismo.submit
import validation.config
from validation.config import batch_sizes, number_of_reruns, generators, get_iterations

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage:\n\tpython {} <name of python script> <compute budget> <other arguments passed to python script>".format(sys.argv[0]))
        print("<compute budget> should be in terms of number of total samples calculated (integer). Reruns not included.")
        exit(1)
    python_script = sys.argv[1]
    compute_budget = int(sys.argv[2])
    for generator in generators:
        for batch_size in batch_sizes:

            if 2 * batch_size > compute_budget:
                continue

            starting_sizes = validation.config.make_starting_sizes(batch_size, compute_budget)

            for starting_size in starting_sizes:
                iterations = get_iterations(starting_size, batch_size, compute_budget)
                starting_sample=0
                for rerun in range(number_of_reruns):
                    prefix = validation.config.make_prefix_main(batch_size=batch_size,
                                                                starting_size=starting_size,
                                                                rerun=rerun,
                                                                generator=generator)


                    chain_name = prefix + python_script

                    number_of_samples_per_iteration = [starting_size]
                    number_of_samples_per_iteration.extend([batch_size for _ in range(iterations)])
                    number_of_samples_per_iteration_str = list(map(str, number_of_samples_per_iteration))



                    command = ismo.submit.Command([sys.executable, python_script])
                    command = command.with_long_arguments(
                        prefix=prefix,
                        chain_name=chain_name,
                        number_of_samples_per_iteration=number_of_samples_per_iteration_str,
                        starting_sample=starting_sample,
                        generator=generator)

                    command_list = command.tolist()
                    command_list.extend(sys.argv[3:])

                    subprocess.run(command_list, check=True)

                    starting_sample += sum(number_of_samples_per_iteration)

                # Now we run the plain old DNN + optimize algorithm
                number_of_samples = 0
                for iteration in range(iterations):
                    number_of_samples += number_of_samples_per_iteration[iteration]
                    starting_sample = 0
                    for rerun in range(number_of_reruns):
                        prefix = validation.config.make_prefix_competitor(batch_size=batch_size,
                                                                           starting_size=starting_size,
                                                                           rerun=rerun,
                                                                           iteration=iteration,
                                                                          generator=generator)

                        chain_name = prefix + python_script

                        command = ismo.submit.Command([sys.executable, python_script])
                        command = command.with_long_arguments(
                            prefix=prefix,
                            chain_name=chain_name,
                            number_of_samples_per_iteration=[str(number_of_samples), str(batch_size)],
                            starting_sample=starting_sample,
                            generator=generator)

                        command_list = command.tolist()
                        command_list.extend(sys.argv[3:])

                        subprocess.run(command_list, check=True)

                        starting_sample += number_of_samples



