import torch

# Constants
G, DT, M = 9.81, 0.02, 1.0

def step(th, om, u, L, b):
    """One semi-implicit Euler step. All args are tensors; L and b may require grad.
    Returns (th_next, om_next)."""
    # TODO(M1): implement using torch ops only

    # Angular acceleration contributors:
        # Gravity:  −(G / L) × sin(th)
        # Damping:  −(b / (M × L²)) × om
        # Motor:     u / (M × L²)

    gravity = -(G / L) * torch.sin(th) # Always pull towards equilibrium
    damping = -(b / (M * L**2)) * om # Always oppose current motion (friction)
    motor = u / (M * L**2) # Always push in the direction of the control input

    # Total angular acceleration
    alpha = gravity + damping + motor

    # Update angular velocity and angle
    om_next = om + alpha * DT
    th_next = th + om_next * DT # Uses the updated angular velocity for semi-implicit Euler

    return th_next, om_next

def rollout(th0, om0, U, L, b):
    """Simulate a batch: th0, om0 shape [n]; U shape [n, T]. Return angles shape [n, T]."""
    # TODO(M1): loop over time with step(); stack the angles

    th, om = th0, om0 # Initialize the current angle and angular velocity
    angles = [] # List to store angles at each time step -- [[n], [n], ...] for T time steps
    T = U.shape[1] # Number of time steps

    for t in range(T):
        u = U[:, t] # Control input at time step t -- shape[n]
        th, om = step(th, om, u, L, b) # Update angle and angular velocity
        angles.append(th) # Store the current angle

    return torch.stack(angles, dim=1) # Stack angles along the time dimension to get shape [n, T]
