# Start here

[README](README.md) · [Begin M0](Learning/M0.md)

Learn PyTorch, build a simulator, fit its physics, train a controller, then test it. Basic Python variables, functions, loops, and lists are enough to begin.

## Setup

1. Follow the [README commands](README.md#run-the-project). A CPU is enough.
2. Open the project folder in your editor. **Project root** means the folder containing README.md and the Python files.
3. In VS Code, select the Python interpreter inside `.venv`. Run commands from the project root with that environment activated.

## Practice

This repository contains completed solutions. Work in your own copy: read the assignment, attempt it, then compare with the reference. Keep the documented function signatures.

Use `MY_WORKLOG.md` for your notes. The existing [WORKLOG.md](WORKLOG.md) preserves my original learning record.

| Guide | Work in | End product |
|---|---|---|
| [M0](Learning/M0.md) | `m0_practice.py` | A model that learns a line |
| [M1](Learning/M1.md) | `sim.py` | A tested pendulum simulator |
| [M2](Learning/M2.md) | `calibrate.py` | Fitted length and damping |
| [M3](Learning/M3.md) | `policy.py` | Two trained controllers |
| [M4](Learning/M4.md) | `evaluate.py` | A fair comparison and explanation |

**Attempt → check → explain → continue.** Ask for a hint when stuck; every guide is available now.

Treat `real_robot.py` as a black box: call its public functions without reading hidden parameters. Save plots in `figures/`, measurements in `results/`, and report actual outcomes.
