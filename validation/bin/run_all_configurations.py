"""
Runs all configuration for analysis
"""

import sys
import os
import subprocess
import ismo.submit
import validation.config
from validation.config import batch_sizes, iterations, number_of_reruns

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage:\n\tpython {} <name of python script> <other arguments passed to python script>".format(sys.argv[0]))
        exit(1)
    python_script = sys.argv[1]
    
    for batch_size in batch_sizes:

        starting_sizes = validation.config.make_starting_sizes(batch_size)

        for starting_size in starting_sizes:
            starting_sample=0
            for rerun in range(number_of_reruns):
                prefix = validation.config.make_prefix_main(batch_size=batch_size,
                                                            starting_size=starting_size,
                                                            rerun=rerun)
                         

                chain_name = prefix + python_script

                number_of_samples_per_iteration = [starting_size]
                number_of_samples_per_iteration.extend([batch_size for _ in range(iterations)])
                number_of_samples_per_iteration_str = list(map(str, number_of_samples_per_iteration))

                

                command = ismo.submit.Command([sys.executable, python_script])
                command = command.with_long_arguments(
                    prefix=prefix,
                    chain_name=chain_name,
                    number_of_samples_per_iteration=number_of_samples_per_iteration_str,
                    starting_sample=starting_sample)

                command_list = command.tolist()
                command_list.extend(sys.argv[2:])

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
                                                                       iteration=iteration)

                    chain_name = prefix + python_script

                    command = ismo.submit.Command([sys.executable, python_script])
                    command = command.with_long_arguments(
                        prefix=prefix,
                        chain_name=chain_name,
                        number_of_samples_per_iteration=[str(number_of_samples), str(batch_size)],
                        starting_sample=starting_sample)

                    command_list = command.tolist()
                    command_list.extend(sys.argv[2:])
                    
                    subprocess.run(command_list, check=True)

                    starting_sample += number_of_samples
            
        
        
