"""
Runs all configuration for analysis
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os
import subprocess
import ismo.submit
import validation.config
import plot_info
from validation.config import batch_sizes, iterations, number_of_reruns, generators

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage:\n\tpython {} <name of python script>")
        exit(1)
    python_script = sys.argv[1]
    for generator in generators:
        for batch_size in batch_sizes:

            starting_sizes = validation.config.make_starting_sizes(batch_size)

            for starting_size in starting_sizes:
                starting_sample=0
                min_value_per_iteration = np.zeros((iterations, number_of_reruns))
                for rerun in range(number_of_reruns):

                    for iteration in range(iterations):
                        output_objective = validation.config.get_objective_filename(batch_size=batch_size,
                                                                                    starting_size=starting_size,
                                                                                    rerun=rerun, iteration=iteration,
                                                                                    generator=generator)

                        values = np.loadtxt(output_objective)

                        min_value = np.min(values)
                        if iteration > 0:
                            min_value = min(min_value, np.min(min_value_per_iteration[:iteration,rerun]))

                        min_value_per_iteration[iteration, rerun] = min_value


                number_of_samples = 0
                min_value_per_iteration_competitor = np.zeros((iterations, number_of_reruns))
                for rerun in range(number_of_reruns):
                    for iteration in range(iterations):
                        all_values = []
                        for pass_number in [0, 1]:
                            output_objective = validation.config.get_competitor_objective_filename(batch_size=batch_size,
                                                                                                   starting_size=starting_size,
                                                                                                   rerun=rerun, iteration=iteration,
                                                                                                   pass_number=pass_number,
                                                                                                   generator=generator)

                            values = np.loadtxt(output_objective)
                            all_values.extend(values)


                        min_value = np.min(all_values)

                        min_value_per_iteration_competitor[iteration, rerun] = min_value

                iteration_range = np.arange(0, iterations)
                plt.errorbar(iteration_range, np.mean(min_value_per_iteration, 1),
                             yerr=np.std(min_value_per_iteration, 1), label='ISMO',
                             fmt='o')

                plt.errorbar(iteration_range, np.mean(min_value_per_iteration_competitor, 1),
                             yerr=np.std(min_value_per_iteration_competitor, 1), label='DNN+Opt',
                             fmt='*')

                plt.xlabel("Iteration $k$")
                plt.ylabel("$\\mathbb{E}( J(x_k^*))$")
                plt.legend()
                plt.title("script: {}, batch_size: {},\nstarting_size: {}".format(
                    python_script, batch_size, starting_size))
                plot_info.savePlot("{script}_objective_{generator}_{batch_size}_{starting_size}".format(
                    script=python_script.replace(".py", ""),
                    batch_size=batch_size,
                    starting_size=starting_size,
                    generator=generator))
                plt.close('all')


