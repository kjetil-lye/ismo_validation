import ismo.submit
import ismo.submit.defaults
import sys
import os


class ProjectileMotionCommands(ismo.submit.defaults.Commands):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def do_evolve(self, submitter,
                  *,
                  iteration_number: int,
                  input_parameters_file: str,
                  output_value_files: list):
        command = ismo.submit.Command([self.python_command, 'evolve_projectile_motion.py'])

        command = command.with_long_arguments(input_parameters_file=input_parameters_file,
                                              output_values_file=output_value_files)

        submitter(command, wait_time_in_hours=24)


if __name__ == '__main__':
    files_to_delete = ['parameters.txt', 'model_{}.h5', 'values_{}.txt',
                       'parameters_for_optimization.txt', 'optimization_results.pic']

    for filename_template in files_to_delete:
        for component in range(1):
            filename = filename_template.format(component)
            if os.path.exists(filename):
                os.remove(filename)

    import argparse

    parser = argparse.ArgumentParser(description="""
Submits all the jobs for the sine experiments
        """)

    parser.add_argument('--number_of_samples_per_iteration', type=int, nargs='+',
                        help='Number of samples per iteration')

    parser.add_argument('--chain_name', type=str, default="projectile_motion",
                        help="Name of the chain to run")

    parser.add_argument('--prefix', type=str, default="",
                        help="Prefix of files")

    parser.add_argument('--submitter', type=str, required=True,
                        help='Submitter to be used. Either "bash" (runs without waiting) or "lsf"')

    parser.add_argument('--dry_run', action='store_true',
                        help="Don't actually run the command, only print the commands that are to be executed")

    parser.add_argument('--starting_sample', type=int, default=0,
                        help='Starting sample')

    parser.add_argument('--generator', type=str, default='monte-carlo',
                        help='Generator name')

    parser.add_argument('--container_type', type=str, default=None,
                        help="Container type (none, docker, singularity)")

    parser.add_argument('--container', type=str, default='docker://kjetilly/machine_learning_base:0.1.2',
                        help='Container name')

    parser.add_argument('--number_of_processes', type=int, nargs='+',
                        help='Ignored, added for compatibility')

    parser.add_argument('--optimizer', type=str, default='L-BFGS-B',
                        help='Name of optimizer')

    args = parser.parse_args()

    submitter = ismo.submit.create_submitter(args.submitter, args.chain_name, dry_run=args.dry_run,
                            container_type=args.container_type,
                            container=args.container)

    commands = ProjectileMotionCommands(dimension=2,
                                        training_parameter_config_file='training_parameters.json',
                                        optimize_target_file='objective.py',
                                        optimize_target_class='Objective',
                                        python_command='python',
                                        starting_sample=args.starting_sample,
                                        prefix=args.prefix,
                                        sample_generator_name=args.generator,
                                        output_append=True,
                                        reuse_model=True,
                                        optimization_results_filename='optimization_results.pic',
                                        optimizer_name=args.optimizer
                                        )

    chain = ismo.submit.Chain(args.number_of_samples_per_iteration, submitter,
                              commands=commands)

    chain.run()
