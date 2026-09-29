import math, torch
from sim import step, rollout

def test_small_angle_period():
    L = torch.tensor(1.0); b = torch.tensor(0.0)
    th, om, t, crossings = torch.tensor([0.05]), torch.tensor([0.0]), 0, []
    prev = th.item()
    for k in range(2000):
        th, om = step(th, om, torch.tensor([0.0]), L, b)
        if prev > 0 >= th.item(): crossings.append(k)
        prev = th.item()
    period = (crossings[1] - crossings[0]) * 0.02
    assert abs(period - 2 * math.pi * math.sqrt(1.0 / 9.81)) < 0.05

def test_gradients_reach_params():
    L = torch.tensor(1.0, requires_grad=True); b = torch.tensor(0.1, requires_grad=True)
    Y = rollout(torch.tensor([0.3]), torch.tensor([0.0]), torch.zeros(1, 50), L, b)
    Y.sum().backward()
    assert L.grad is not None and b.grad is not None
