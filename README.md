# sim2real-pendulum — a tiny real-to-sim-to-real loop in PyTorch

**New here? Start with [Learning/START HERE.md](Learning/START%20HERE.md).** Your working folder is
`~/Desktop/Projects/sim2real-pendulum`; its `Sim2Real Guide/` folder contains the video,
transcript, and learning shortcuts.

**Goal (2–3 evenings):** use a small amount of "real robot" data to calibrate a differentiable
simulator, train a controller in simulation, and show it transfers to the "real" system better
than a controller trained in an uncalibrated simulator.
This is a toy version of the RoboSim idea (real data → task-specific simulator → better policy → back to real).

The "real robot" is `real_robot.py`: a pendulum whose true length and damping are hidden.
Treat it like hardware — you may only call its functions, not read its parameters.

## Physics (you already know this from Physics 2A / ODEs)
θ'' = −(g/L)·sin θ − (b/(m L²))·θ' + u/(m L²),  with m = 1, g = 9.81, dt = 0.02 s.
Integrate with **semi-implicit Euler**: ω ← ω + dt·θ'',  then θ ← θ + dt·ω.

## Milestones (tick them off in order)
- [ ] **M0 — PyTorch basics (~2 h).** Official "Learn the Basics" tutorial: tensors, autograd, `nn.Module`, optimizers.
- [ ] **M1 — Differentiable simulator (`sim.py`).** Implement `step` and `rollout` with torch ops only (no numpy), batched over trajectories.
      Check: `pytest -q` passes (small-angle period ≈ 2π√(L/g); gradients reach L and b).
- [ ] **M2 — Real-to-sim calibration (`calibrate.py`).** Start from the nominal guess L = 1.0, b = 0.1.
      Optimize log L and log b with Adam so simulated θ(t) matches the real trajectories (MSE).
      Report the recovered values and plot loss vs. iteration.
- [ ] **M3 — Policy in sim (`policy.py`).** Task: hold the pendulum at θ = 0.6 rad (needs a steady gravity-compensating torque).
      Policy = small MLP on (θ − target, ω), torque = 10·tanh(output).
      Train by **backpropagating the task cost through your simulator** (no RL library needed).
      Train two policies: one in the nominal sim, one in the calibrated sim.
- [ ] **M4 — Sim-to-real evaluation (`evaluate.py`).** Run both on the real robot; report steady-state |error| (mean over the last 100 steps).
      Expected outcome: the calibrated-sim policy has a clearly smaller error. Explain *why* in 3–4 sentences.
- [ ] **M5 — Write-up.** Fill in "Results" below (numbers + one plot), push to GitHub.

## Results (fill in — only numbers you actually produced)
| | L | b | steady-state error on real (rad) |
|---|---|---|---|
| nominal sim | 1.0 | 0.1 | |
| calibrated sim | | | |

What I learned / what surprised me:

## Stretch (only if time)
- Calibrate with fewer real trajectories (4? 2?) — how much real data is enough?
- Add sensor noise to training (domain randomization) instead of calibrating — compare.
- Replace backprop-through-sim with a basic policy-gradient (REINFORCE) method and compare sample efficiency.
