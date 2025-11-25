from typing import Tuple

Vec = Tuple[float, float]

# add and scale vector are helpers that make updating vectors easier

def add_vec(a, b):
    return [a[0] + b[0], a[1] + b[1]]


def scale_vec(v, s):
    return [v[0] * s, v[1] * s]

# equation for drag force
def drag_force(vel, drag_coeff):
    return [-drag_coeff * vel[0], -drag_coeff * vel[1]]

# acceleration computations for moving positions 
def compute_accel(gravity, mass, drag_coeff, vel):
    # acceleration = gravity + drag/mass
    df = drag_force(vel, drag_coeff)
    drag_over_mass = [df[0]/mass, df[1]/mass]
    return add_vec(gravity, drag_over_mass)    

# This physics part really just shows how different variables will
# affect how fast or slow the object is going horizontally and vertically

# eulers method is a algoritm here that approximates the motion of objects
# from the inital point to the goal state by using slope at each point to 
# estimate the next point 
def euler_integrator(pos, vel, dt, gravity, mass, drag_coeff):
    # compute new velocity by adding acceleration times dt
    # updated_velocity = vel + compute_accel(gravity, mass, drag_coeff, vel) * dt

    updated_velocity = add_vec(vel, scale_vec(compute_accel(gravity, mass, drag_coeff, vel), dt))

    # update the position by adding the new movement to the position
    # updated_position = pos + updated_velocity * dt

    updated_position = add_vec(pos, scale_vec(updated_velocity, dt))

    return updated_position, updated_velocity

    #later change these to use the scale and add vectors, as just doing this will give error