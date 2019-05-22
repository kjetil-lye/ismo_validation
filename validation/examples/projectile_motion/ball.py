import numpy as np

def right_hand_side(u, rho, C_D, r, m, g):
    v_vec = u[2:]
    norm_v = np.linalg.norm(v_vec)
    v_normalized = v_vec / norm_v
    
    A = np.pi * r**2
    
    drag = 0.5 * rho * C_D * norm_v **2 * A
    
    return np.array([v_vec[0], 
                     v_vec[1],
                     -drag/m * v_normalized[0], 
                     -drag/m * v_normalized[1] - g, 
                    ])

def simulate_until_impact(h_0, x_0, v_0, alpha, g, C_D, rho, dt, r, m):
    # We need to solve an ODE
    u_0 = np.array([x_0, h_0, v_0*np.cos(alpha), v_0*np.sin(alpha)])
    
    # WARNING: This is not the most effective way of doing this
    # but it is used for educational purposes.
    t = [0]
    u = [u_0]
    
    
    while u[-1][1] > 0:
        u.append(u[-1] + dt * right_hand_side(u[-1], rho, C_D, r, m, g))
        
        t.append(t[-1] + dt)

    return np.array(u), np.array(t)

@np.vectorize
def p(h_0, x_0, v_0, alpha, g, C_D, rho, dt, r, m):
    u, t = simulate_until_impact(h_0, x_0, v_0, alpha, g, C_D, rho, dt, r, m)
    
    return [u[-1][0], t[-1]]

import sys


def p_alpha_v_0_samples(h_0, x_0, v_0, alpha, g, C_D, rho, dt, r, m):
    u = np.zeros(alpha.shape[0])
    t = np.zeros(alpha.shape[0])
    
    for i in range(alpha.shape[0]):
        u_temp, t_temp = p(h_0, x_0, float(v_0[i]),
                           float(alpha[i]), g, C_D, rho, dt, r, m)
            
        u[i] = u_temp
        t[i] = t_temp

    return u, t
