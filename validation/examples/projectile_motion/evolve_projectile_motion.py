import numpy as np
import ball
if __name__ == '__main__':
    # Parameters we use
    x_0 = 0.2
    h_0 = 0.5
    g = 9.81
    C_D = 0.1
    m = 0.142
    r = 0.22
    rho = 1.1455
    dt = 0.01

    
    import argparse

    parser = argparse.ArgumentParser(description="""
Runs the function sin(4*pi*x) on the input parameters
    """)

    parser.add_argument('--input_parameters_file', type=str, required=True,
                        help='Input filename for the parameters (readable by np.loadtxt)')

    parser.add_argument('--output_values_file', type=str, required=True,
                        help='Output filename for the values (will be written by np.savetxt)')

    args = parser.parse_args()

    parameters = np.loadtxt(args.input_parameters_file)

    values = ball.p_alpha_v_0_samples(h_0, x_0,
                                      parameters[:,0],
                                      parameters[:,1],
                                      g, C_D, rho, dt, r, m)
    
    np.savetxt(args.output_values_file, values)
