import torch
from sim import step
TARGET, UMAX = 0.6, 10.0

def make_policy():
    return torch.nn.Sequential(torch.nn.Linear(2, 32), torch.nn.Tanh(), torch.nn.Linear(32, 1))

def train_policy(L, b, iters=300, lr=0.01, seed=1):
    """Train by backpropagating the task cost through the differentiable simulator."""
    torch.manual_seed(seed)
    policy = make_policy()
    # TODO(M3): each iteration - sample a batch of start angles near 0,
    # roll out ~150 steps with u = UMAX*tanh(policy([th-TARGET, om])),
    # cost = mean((th-TARGET)^2) + 0.01*mean(om^2) over time; backprop; Adam step.
    raise NotImplementedError
