import numpy as np
import os
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="""
Runs the function sin(4*pi*x) on the input parameters
    """)

    parser.add_argument('--input_parameters_file', type=str, required=True,
                        help='Input filename for the parameters (readable by np.loadtxt)')

    parser.add_argument('--output_values_file', type=str, required=True,
                        help='Output filename for the values (will be written by np.savetxt)')

    parser.add_argument('--start', type=int, default=0,
                        help='Starting index to read out of the parameter file, by default reads from start of file')

    parser.add_argument('--end', type=int, default=-1,
                        help='Ending index (exclusive) to read out of the parameter file, by default reads to end of file')

    parser.add_argument('--output_append', action='store_true',
                        help='Append output to end of file')


    args = parser.parse_args()

    if args.end != -1:
        parameters = np.loadtxt(args.input_parameters_file)[args.start:args.end]
    else:
        parameters = np.loadtxt(args.input_parameters_file)[args.start:]

    values = np.sin(4 * np.pi * parameters)

    values_to_write = values[:]
    if args.output_append:
        if os.path.exists(args.output_values_file):
            previous_values = np.loadtxt(args.output_values_file)

            new_values = np.zeros((values.shape[0] + previous_values.shape[0]))

            new_values[:previous_values.shape[0]] = previous_values
            new_values[previous_values.shape[0]:] = values

            values_to_write = new_values
    np.savetxt(args.output_values_file, values_to_write)
