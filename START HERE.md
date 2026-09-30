# Start here — your Sim2Real Pendulum project

Your working folder is **Desktop → Projects → sim2real-pendulum**.
Everything you need to begin is here. All milestones are still yours to complete.

## First, get oriented

1. Open **Sim2Real Guide → Open Project.command** to launch this folder in VS Code.
2. Watch [the walkthrough](Sim2Real%20Guide/pendulum-walkthrough.mp4), or read [its transcript](Sim2Real%20Guide/walkthrough-transcript.md).
3. Read [README.md](README.md) for the exercise instructions. Use [WORKLOG.md](WORKLOG.md) for your own learning notes.

The guide's ZIP and **Original Desktop Starter** are untouched backups. Write code in the working files beside this page. Backup tests are excluded from normal test discovery.

## Your first session: M0 only

Aim to understand one small idea, not finish the entire project today.

1. Open the [official PyTorch Learn the Basics tutorial](https://docs.pytorch.org/tutorials/beginner/basics/intro.html). Begin with **Tensors**, then **Automatic Differentiation**. You can return to the other sections later.
2. In VS Code, create your own `m0_practice.py` in the project root. This is a practice file; leave the milestone TODOs alone for now.
3. Try creating a tensor, performing a simple operation, and inspecting its shape and value. Then try a scalar expression with gradient tracking and compare its computed derivative with your hand calculation.
4. Run your practice file in the terminal using the environment below.
5. In the M0 section of WORKLOG.md, write what a tensor is, what a gradient tells you, and one question you still have. Update the status truthfully.

Later in M0, learn what `nn.Module` and an optimizer do. Move to M1 when you can explain your small experiments and the basic roles of those tools in your own words.

## Run code in the right environment

In VS Code, choose **Terminal → New Terminal**. Run:

```sh
cd "$HOME/Desktop/Projects/sim2real-pendulum"
source .venv/bin/activate
python -c "import sys; print(sys.executable)"
```

The printed path should end in `Desktop/Projects/sim2real-pendulum/.venv/bin/python`.
After you create your practice file, run `python m0_practice.py`.

VS Code is configured to use this `.venv`. It contains Python packages, including PyTorch; it does not belong on GitHub.

## How a small step contributes

| Milestone | Your task | Evidence you build for the final experiment |
|---|---|---|
| M0 | Learn tensors, gradients, modules, and optimizers | Small experiments you can explain |
| M1 | Implement `step` and `rollout` in `sim.py` | A simulator checked by `test_sim.py` |
| M2 | Implement calibration in `calibrate.py` | Estimated parameters and a loss history based on observed data |
| M3 | Train controllers in `policy.py` | One controller from nominal simulation and one from calibrated simulation |
| M4 | Run `evaluate.py` after its dependencies are implemented | A comparison on the same reference system |
| M5 | Explain actual findings in README.md | Real plots, measured errors, and reproducible conclusions |

`real_robot.py` is a software stand-in for hardware. Use its public functions, not its hidden parameters. Better transfer is a hypothesis to test, not a guaranteed result.

Run `pytest -q` for the simulator checks. Before M1 is implemented, **two `NotImplementedError` failures are expected**. M0 practice does not make those tests pass.

## Your everyday cycle

**Read one task → write a small change → save → run a relevant check → explain what happened → commit → push.**

Saving changes files on your Mac. A Git commit records a local checkpoint. A push sends your commits to your [private GitHub repository](https://github.com/HEGOBAK/sim2real-pendulum).

When you have meaningful progress, run `git status`, inspect `git diff`, stage the specific files you changed with `git add`, and commit with an accurate message. Then run `git push`. Do not claim a milestone is complete until you have done and checked it.

Keep small experimental plots in `figures/` and final tables in `results/`. Write only your actual results in the README. No exercise implementation or results have been supplied by this guide.
