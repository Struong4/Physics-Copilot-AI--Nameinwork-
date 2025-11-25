import numpy as np

# using numpy that shapes numpy arrays into [x,y]

# equation for drag force
def drag_force(vel: np.ndarray, drag_coeff: float) -> np.ndarray:
    # takes drag force and multiplies it by velocity which is a numpy array
    # and then returns a numpy array of [Fx, Fy]
    return -drag_coeff * vel

# acceleration computations for moving positions 
def compute_accel(gravity: np.ndarray, mass: float, drag_coeff: float, vel: np.ndarray) -> np.ndarray:
    # acceleration = gravity + drag/mass
    # returns numpy array in same format for drag_force
    df = drag_force(vel, drag_coeff)
    drag_over_mass = df / mass
    return gravity + drag_over_mass

# This physics part really just shows how different variables will
# affect how fast or slow the object is going horizontally and vertically

# eulers method is a algoritm here that approximates the motion of objects
# from the inital point to the goal state by using slope at each point to 
# estimate the next point 
def euler_integrator(pos: np.ndarray, vel: np.ndarray, dt: float,
                     gravity: np.ndarray, mass: float, drag_coeff: float):
    # compute new velocity by adding acceleration times dt
    # updated_velocity = vel + compute_accel(gravity, mass, drag_coeff, vel) * dt

    updated_velocity = vel + compute_accel(gravity, mass, drag_coeff, vel) * dt

    # update the position by adding the new movement to the position
    # updated_position = pos + updated_velocity * dt

    updated_position = pos + updated_velocity * dt

    return updated_position, updated_velocity

    #later change these to use the scale and add vectors, as just doing this will give error