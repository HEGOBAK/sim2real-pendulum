# Sim2Real Pendulum

**Can fitting a simulator to observed motion improve a controller's performance on a separate reference system?** This small PyTorch project follows that question from differentiable physics to system identification, controller training, and evaluation.

In the recorded comparison, calibration reduced mean holding error from **0.036721 rad to 0.004281 rad — an 88.34% reduction**. The reference system is a software stand-in for a pendulum; this is a simulation study, with no physical robot involved.

**Learning from scratch? → [Start here](START_HERE.md)** for setup and the M0–M4 assignments. **Reviewing the project?** The results, method, and reproduction commands are below. The repository includes completed implementations and the author's original [learning notes](WORKLOG.md), including corrections.

## Experiment

```text
Observed motion from the reference system
                   ↓
Fit simulator length L and damping b
                   ↓
Train two controllers: nominal simulator vs. calibrated simulator
                   ↓
Evaluate both on the same reference system
```

Calibration and control learn different quantities. Calibration adjusts two physical parameters to match measured angle trajectories. Controller training holds those physical parameters fixed and adjusts neural-network weights and biases to choose motor torque.

| Stage | Implementation | What it does |
|---|---|---|
| Physics | [sim.py](sim.py) | Batched pendulum steps and rollouts that preserve gradients |
| Identification | [calibrate.py](calibrate.py) | Fits positive L and b through their logarithms using trajectory MSE and Adam |
| Control | [policy.py](policy.py) | Trains a 2 → 32 → 1 network through the differentiable simulator |
| Evaluation | [evaluate.py](evaluate.py) | Compares both policies, validates errors, and saves measurements |

The simulator uses

$$\ddot{\theta} = -\frac{g}{L}\sin\theta - \frac{b}{mL^2}\dot{\theta} + \frac{u}{mL^2},$$

with mass `m = 1`, gravity `g = 9.81`, and time step `dt = 0.02 s`. Semi-implicit Euler updates angular velocity before angle. The controller receives angle error and angular velocity, aims to hold **0.6 rad**, and produces torque bounded by `10 × tanh(network output)`.

During training, the objective is the average of `(angle − target)² + 0.01 × angular_velocity²` across trajectories and time. There are no correct-torque labels: gradients pass through the simulated motion to the policy parameters.

## Recorded results

Both controllers were evaluated on the reference system with errors shaped **(256 trajectories, 300 steps)**. The metric below averages absolute target-angle error over all trajectories and the **last 100 steps**. It measures late holding performance, not the entire transient response or a proven steady state.

| Controller trained in | Simulator L | Simulator b | Mean holding error (rad) |
|---|---:|---:|---:|
| Nominal simulator | 1.000000 | 0.100000 | 0.036721 |
| Calibrated simulator | 1.199742 | 0.351047 | 0.004281 |

Source: [full-precision measurements and settings](results/m4_comparison.csv).

- **Absolute reduction:** nominal error − calibrated error = **0.032440 rad**.
- **Relative reduction:** absolute reduction / nominal error × 100 = **88.34%**.

Fitting observed motion gives the controller a training simulator closer to the reference dynamics. The lower reference error supports improved transfer for this experiment. It does not establish exact recovery of hidden parameters, reliability across other seeds or operating conditions, or performance on physical hardware. The averaged final window can also hide early overshoot, settling-time differences, and poor individual trajectories.

![Training cost for policies trained in nominal and calibrated simulators](figures/m3_training_comparison.png)

*Training cost over 300 optimizer updates, measured separately in each policy's training simulator. Both policies learn, but these curves alone cannot establish which transfers better; the reference-system comparison above provides that evidence.*

The [calibration loss plot](figures/m2_calibration_loss.png) separately records fitting error. The reviewed calibration run reduced trajectory MSE from approximately `0.02783` to `0.00010067`.

## Reproduce the experiment

Run commands from the **project root**, the folder containing this README and `evaluate.py`. A CPU is sufficient. The recorded environment used Python 3.12.14, PyTorch 2.14.0, Matplotlib 3.11.2, and pytest 9.1.1. Dependencies in `requirements.txt` are unpinned, so a new installation may resolve different versions; exact floating-point results can vary.

```sh
git clone https://github.com/HEGOBAK/sim2real-pendulum.git
cd sim2real-pendulum
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python evaluate.py
```

On Windows PowerShell, use `py -m venv .venv` and `.\.venv\Scripts\Activate.ps1` instead of the environment creation and activation commands above.

`evaluate.py` performs calibration, trains both policies, then evaluates them. There is no need to run every Python file separately. It saves `results/m4_comparison.csv` and `figures/m3_training_comparison.png`; rerunning replaces those files. Progress may be quiet while training runs.

To regenerate the separate calibration plot:

```sh
python calibrate.py
```

This writes `figures/m2_calibration_loss.png`. For a machine without a display, prefix plotting commands with `MPLBACKEND=Agg` on macOS/Linux.

| Setting | Recorded value |
|---|---|
| Calibration | Adam, 400 updates, learning rate 0.05 |
| Policy training | Adam, 300 updates, learning rate 0.01 |
| Training batch / horizon | 32 trajectories / 150 steps |
| Training starts | Angles uniform in [−0.1, 0.1), zero angular velocity |
| Training seed | 1 for both policies |
| Evaluation seed set by caller | 123 before each reference call |
| Reference evaluation | 256 trajectories / 300 steps; same target and call settings |

The two simulator tests cover the small-angle period and gradient connectivity to L and b. Evaluation also rejects malformed, nonfinite, or negative absolute-error tensors. These checks support the implementation; they are not exhaustive physical validation.

## Learn by rebuilding

Follow [START_HERE.md](START_HERE.md) to attempt each assignment in order. The completed source is a reference solution; the guides explain how to practice in your own copy without needing an assistant to unlock later milestones.

| Milestone | Assignment | Deliverable |
|---|---|---|
| [M0](Learning/M0.md) | PyTorch basics | Fit `y = 2x + 1` and explain the gradient path |
| [M1](Learning/M1.md) | Differentiable physics | Batched simulator with passing checks |
| [M2](Learning/M2.md) | System identification | Fitted L and b and calibration loss plot |
| [M3](Learning/M3.md) | Controller training | Nominal and calibrated policies and training curves |
| [M4](Learning/M4.md) | Reference evaluation | Reproducible comparison and a justified conclusion |

All five milestones are implemented in this repository. Treat `real_robot.py` as a black box while learning: use its public data-collection and evaluation functions rather than looking up the hidden parameters. [WORKLOG.md](WORKLOG.md) preserves the learning process, including initial misunderstandings and subsequent feedback.
