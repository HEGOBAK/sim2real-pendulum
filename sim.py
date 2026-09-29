import torch
G, DT, M = 9.81, 0.02, 1.0

def step(th, om, u, L, b):
    """One semi-implicit Euler step. All args are tensors; L and b may require grad.
    Returns (th_next, om_next)."""
    # TODO(M1): implement using torch ops only
    raise NotImplementedError

def rollout(th0, om0, U, L, b):
    """Simulate a batch: th0, om0 shape [n]; U shape [n, T]. Return angles shape [n, T]."""
    # TODO(M1): loop over time with step(); stack the angles
    raise NotImplementedError
