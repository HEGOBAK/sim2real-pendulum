# Start here — learn the Sim2Real pendulum

[Project overview and results](README.md) · [Begin M0](Learning/M0.md)

Build one small experiment: learn PyTorch, simulate a pendulum, fit its physics to observed motion, train a controller, then compare its performance on a separate reference system. The reference is software, so no hardware or GPU is required.

## 1. Set up your workspace

Follow the [README setup commands](README.md#reproduce-the-experiment), then open the repository folder in your editor. **Project root** means the folder containing `README.md`, `sim.py`, and `evaluate.py`. Run your terminal commands there. `.venv` holds your Python environment; `Learning/` holds these assignments.

If using VS Code, choose **Python: Select Interpreter** from the command palette and select the interpreter inside `.venv`. You can check the active terminal interpreter with:

```sh
python -c "import sys; print(sys.executable)"
```

## 2. Choose how to practice

This repository contains completed solutions, not empty starter files. To learn independently, fork or copy it into your own working folder and keep the original version as a reference. For each milestone, read the assignment first, write your own implementation in the named file, and compare only after an attempt. Keep the documented function signatures so later stages and supplied tests still work. Do not overwrite someone else's working copy.

Start a separate personal notes file, such as `MY_WORKLOG.md`, with sections M0 through M4. The existing [WORKLOG.md](WORKLOG.md) is the author's historical record; it includes mistakes followed by corrections and is useful for comparison after your own attempt.

You only need basic Python variables, loops, functions, and lists to begin. Look up syntax as needed. M0 introduces tensors, gradients, a model, and an optimizer with a concrete self-test; you do not need to finish every PyTorch tutorial first.

## 3. Follow the milestones

| Order | Guide | Work in | Finish when |
|---|---|---|---|
| 0 | [PyTorch basics](Learning/M0.md) | `m0_practice.py` | You fit a line and explain how its parameters learn |
| 1 | [Differentiable simulator](Learning/M1.md) | `sim.py` | Physics, batch, and gradient checks pass |
| 2 | [System identification](Learning/M2.md) | `calibrate.py` | Fitting loss falls and you can explain the learned parameters |
| 3 | [Controller training](Learning/M3.md) | `policy.py` | A trained controller reaches and holds the target in its simulator |
| 4 | [Reference evaluation](Learning/M4.md) | `evaluate.py` | Both controllers are compared fairly and the results are explained |

Every guide is available now. Follow its completion checks, then click **Next**. Learning status is personal: a completed repository does not mean you have completed the exercises yourself.

## 4. Use a short learning cycle

**Read the assignment → attempt it → run its checks → explain the outcome → continue.**

Keep each milestone's measured results and a few sentences about what you learned. Ask a tutor for a hint or code review if stuck; no tutor is required to access the next guide. A useful request is: “Review my saved attempt, explain the first issue, and give one hint without writing the solution.”

The root's `test_sim.py` checks simulator behavior. Its tests pass in the completed repository; when rebuilding M1, failures help locate unfinished or incorrect physics. Run the milestone-specific checks too—passing two simulator tests alone does not validate calibration or control.

## Keep the experiment focused

Use the public `collect_real_data` and `run_policy_on_real` functions in `real_robot.py`; do not inspect hidden physics values to solve the exercise. Compare controllers under matching conditions and report measured outcomes even if calibration does not help. Skip CNNs, DataLoaders, RL libraries, and GPU setup for this project.

Save small plots in `figures/` and result tables in `results/`. A save updates a file, a Git commit records a checkpoint, and a push uploads commits to your own remote. Keep environments and caches out of Git.

**Ready? Start [M0 — PyTorch basics](Learning/M0.md).**
