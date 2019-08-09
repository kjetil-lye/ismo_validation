import matplotlib
matplotlib.use('Agg')
import ismo.convergence

import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
import numpy as np
import ismo.iterative_surrogate_model_optimization
import ismo.train.trainer_factory
import ismo.train.multivariate_trainer
import ismo.samples.sample_generator_factory
import ismo.optimizers
import matplotlib.pyplot as plt
import plot_info

class Objective:
    def __call__(self, x):
        return x

    def grad(self, x):
        return np.ones_like(x)


class Simulator:
    def __call__(self, x):
        return np.sin(4 * np.pi * x)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="""
Runs the function sin(4*pi*x) on the input parameters
        """)

    parser.add_argument('--number_of_samples_per_iteration', type=int, nargs='+', default=[16, 4, 4, 4, 4, 4],
                        help='Number of samples per iteration')

    parser.add_argument('--generator', type=str, default='monte-carlo',
                        help='Generator')

    parser.add_argument('--simple_configuration_file', type=str, default='training_parameters.json',
                        help='Configuration of training and network')

    parser.add_argument('--optimizer', type=str, default='L-BFGS-B',
                        help='Configuration of training and network')

    parser.add_argument('--retries', type=int, default=1,
                        help='Number of retries (to get mean/variance). This option is studying how well it works over multiple runs.')

    parser.add_argument('--save_result', action='store_true',
                        help='Save the result to file')

    parser.add_argument('--prefix', type=str, default="experiment_",
                        help="Prefix to all filenames")

    parser.add_argument('--with_competitor', action='store_true',
                        help='Also run the standard DNN+Opt competitor to see how well ISMO is doing in comparison')

    args = parser.parse_args()
    prefix = args.prefix
    
    
    dimension = 1
    number_of_variables = 1
    
    objective = Objective()
    
    ismo.convergence.convergence_study(
        generator_name = args.generator,
        training_parameter_filename = args.simple_configuration_file,
        optimizer_name = args.optimizer,
        retries = args.retries,
        save_result = args.save_result,
        prefix = args.prefix,
        with_competitor = args.with_competitor,
        dimension = dimension,
        number_of_variables = number_of_variables,
        number_of_samples_per_iteration = args.number_of_samples_per_iteration,
        simulator_creator = lambda starting_sample: Simulator(),
        objective = objective,
        variable_names = ['u'],
        save_plot=plot_info.savePlot
    )

