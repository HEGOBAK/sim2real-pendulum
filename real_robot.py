"""The 'real robot'. Treat as hardware: call the functions, don't read the constants."""
import torch
_G, _DT, _M = 9.81, 0.02, 1.0
_L, _B = 1.2, 0.35   # hidden ground truth - do not use in your code

def _step(th, om, u):
    I = _M * _L * _L
    om = om + _DT * (-(_G / _L) * torch.sin(th) - (_B / I) * om + u / I)
    return th + _DT * om, om

def collect_real_data(n=32, T=100, seed=0):
    """Returns (th0, om0, U, Y): initial states, applied torques [n,T], measured angles [n,T] (noisy)."""
    g = torch.Generator().manual_seed(seed)
    th0 = (torch.rand(n, generator=g) - 0.5) * 2.0
    om0 = (torch.rand(n, generator=g) - 0.5) * 2.0
    U = torch.cumsum(torch.randn(n, T, generator=g) * 0.6, 1).clamp(-4, 4)
    th, om, ys = th0.clone(), om0.clone(), []
    with torch.no_grad():
        for t in range(T):
            th, om = _step(th, om, U[:, t]); ys.append(th)
    Y = torch.stack(ys, 1) + 0.01 * torch.randn(n, T, generator=g)
    return th0, om0, U, Y

def run_policy_on_real(policy, target=0.6, umax=10.0, n=256, T=300, seed=2):
    """Runs a policy (callable on [n,2] tensor of (th-target, om)) on the real robot; returns |error| [n,T]."""
    g = torch.Generator().manual_seed(seed)
    th = (torch.rand(n, generator=g) - 0.5) * 0.6; om = torch.zeros(n); errs = []
    with torch.no_grad():
        for t in range(T):
            u = umax * torch.tanh(policy(torch.stack([th - target, om], 1)).squeeze(1))
            th, om = _step(th, om, u); errs.append((th - target).abs())
    return torch.stack(errs, 1)
