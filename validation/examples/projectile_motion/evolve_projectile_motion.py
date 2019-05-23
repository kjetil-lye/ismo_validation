import numpy as np
import ball

def scale(y, a, b):
    """
    Scales the vector y (assumed to be in [0,1]) to [a,b]
    :param y:
    :param a:
    :param b:
    :return:
    """

    return a*y + (b-a)*y

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
                                      scale(parameters[:,0], 10, 30),
                                      scale(parameters[:,1], 0, np.pi/2),
                                      g, C_D, rho, dt, r, m)
    
    np.savetxt(args.output_values_file, values)
