# Sim2Real Pendulum

I started this project while learning the basics of PyTorch. At first, I was trying to understand how passing an input through a model produces an output, and how the loss connects back to the parameters. Working through this pendulum project helped me see how those same ideas can be used to learn about a physical system and control its motion.

The goal is to bring a pendulum to **0.6 radians** and keep it there. I wanted to understand whether a controller would perform better if its training simulator had first been adjusted using observations from the system it would later control. In this experiment, that adjustment reduced the measured holding error by **88.34%**.

The “real robot” here is a software pendulum in `real_robot.py`. It acts as the reference system for collecting data and testing the controllers. This project does not use physical hardware.

If you are also starting from the basics, I have kept the learning path from **M0 to M4**. Begin with [START_HERE.md](START_HERE.md), then work through each assignment in order. My [WORKLOG.md](WORKLOG.md) contains the questions I had, my attempts to explain them, and the corrections along the way.

## How the project works

The process is:

```text
Collect motion data from the reference pendulum
                   ↓
Adjust the simulator's length L and damping b to match that motion
                   ↓
Train a controller in the adjusted simulator
                   ↓
Test it on the reference pendulum and compare it with the baseline
```

The baseline uses a **nominal simulator**, which starts with a guess of `L = 1.0` and `b = 0.1`. The **calibrated simulator** uses values fitted from the observed motion. Both controllers have the same network structure and training settings; the difference is the simulator they learn in.

One distinction I had to work through was what we are actually learning at each stage. During calibration, we adjust length and damping so the predicted motion matches the measured motion. During controller training, length and damping stay fixed, and we adjust the network's weights and biases so it chooses useful motor torques.

| File | What it does |
|---|---|
| [sim.py](sim.py) | Predicts the next angle and angular velocity, then repeats those steps to simulate a trajectory |
| [calibrate.py](calibrate.py) | Fits L and b by comparing simulated angles with measured angles |
| [policy.py](policy.py) | Trains a network to choose torque from angle error and angular velocity |
| [evaluate.py](evaluate.py) | Tests both controllers on the reference system and saves their errors |

## From physics to a controller

The pendulum's angular acceleration is:

$$\ddot{\theta} = -\frac{g}{L}\sin\theta - \frac{b}{mL^2}\dot{\theta} + \frac{u}{mL^2}.$$

The three terms account for gravity, damping, and motor torque. Here, `m = 1`, `g = 9.81`, and each time step is `0.02 s`. The simulator first updates angular velocity, then uses that new velocity to calculate the next angle. This is the semi-implicit Euler method.

Calibration uses Adam to minimize the mean squared error between predicted and measured angle trajectories. The trainable values are `log_L` and `log_b`; taking their exponentials gives positive L and b for the simulator.

The controller is a **2 → 32 → 1** network. Its two inputs are the difference from the target angle and the current angular velocity. The output is converted into motor torque using `10 × tanh(network output)`, keeping the torque within [−10, 10].

There is no list of correct torques for the network to copy. Instead, the torque affects the next state of the pendulum, and we measure how that motion performs. The training cost averages the following across trajectories and time steps:

```text
(angle − target)² + 0.01 × angular_velocity²
```

The first part encourages the pendulum to stay close to the target. The second discourages excessive motion. Because the simulator uses differentiable PyTorch operations, the cost connects back through the motion and torque to the network's parameters. Backpropagation calculates their gradients, and Adam updates them.

## What I found

I compared both controllers on the same reference system. Each evaluation returned absolute angle errors with shape **(256, 300)**: 256 trajectories, each with 300 time steps. I averaged all trajectories over the **last 100 steps** to measure how well the controllers held the target after the initial movement.

| Controller trained in | Simulator L | Simulator b | Mean holding error (rad) |
|---|---:|---:|---:|
| Nominal simulator | 1.000000 | 0.100000 | 0.036721 |
| Calibrated simulator | 1.199742 | 0.351047 | 0.004281 |

The full values and settings are saved in [m4_comparison.csv](results/m4_comparison.csv).

```text
Absolute reduction = nominal error − calibrated error
                   ≈ 0.032440 rad

Relative reduction = absolute reduction / nominal error × 100
                   ≈ 88.34%
```

The calibrated controller stayed closer to the target in this comparison. This supports the idea that learning in a simulator closer to the reference dynamics can improve performance when the controller is transferred to that system.

![Training costs for the nominal and calibrated controllers](figures/m3_training_comparison.png)

Both curves show training cost over 300 updates, each measured in its own simulator. They show the controllers learning, but the table above is what I use to compare performance on the reference system. A lower training curve alone would not establish better transfer.

The separate [calibration loss plot](figures/m2_calibration_loss.png) shows how closely the simulator fits the observed motion. In the reviewed run, trajectory MSE fell from about `0.02783` to `0.00010067`.

## What this result tells me

The main connection for me is that the simulator becomes part of the learning process. In calibration, gradients tell us how to change the physical parameters to match motion. In controller training, gradients pass through that motion to tell us how to change the network's decisions. The same idea from fitting a line in M0 carries through both stages.

The result also has limits. This is one training seed and one evaluation setup on a software reference system. It does not prove that the fitted parameters are exactly correct, that calibration always helps, or that the controller would work on physical hardware. Averaging the last 100 steps can also miss early overshoot, differences in settling time, or individual trajectories with large errors.

## Run the project

Run these commands from the project root, which is the folder containing this README and `evaluate.py`. A CPU is enough.

```sh
git clone https://github.com/HEGOBAK/sim2real-pendulum.git
cd sim2real-pendulum
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python evaluate.py
```

On Windows PowerShell, use `py -m venv .venv` and `.\.venv\Scripts\Activate.ps1` for environment creation and activation.

You only need to run `evaluate.py` for the full comparison. It runs calibration, trains both controllers, and evaluates them. Training may take a while without printing progress. The outputs are:

- `results/m4_comparison.csv`: measured errors and experiment settings.
- `figures/m3_training_comparison.png`: both training-cost curves.

Running it again replaces those files. To regenerate the separate calibration plot, run:

```sh
python calibrate.py
```

This saves `figures/m2_calibration_loss.png`. On macOS/Linux without a display, prefix either plotting command with `MPLBACKEND=Agg`.

The recorded environment used **Python 3.12.14, PyTorch 2.14.0, Matplotlib 3.11.2, and pytest 9.1.1**. `requirements.txt` does not pin package versions, so a fresh installation may use different versions and produce slightly different numerical results.

| Setting | Value used |
|---|---|
| Calibration | Adam, 400 updates, learning rate 0.05 |
| Controller training | Adam, 300 updates, learning rate 0.01 |
| Training batch / horizon | 32 trajectories / 150 steps |
| Training starting states | Angles uniform in [−0.1, 0.1), zero angular velocity |
| Training seed | 1 for both controllers |
| Evaluation seed set by the caller | 123 before each reference call |
| Reference evaluation | 256 trajectories / 300 steps, same target and call settings |

The two simulator tests check the small-angle period and whether gradients reach L and b. Evaluation also checks the error tensor's shape and rejects nonfinite or negative absolute errors. These are useful checks, but they do not cover every possible behavior of the system.

## Follow the learning path

The repository contains completed implementations. If you want to learn by doing it yourself, [start here](START_HERE.md) and attempt each assignment in your own copy before comparing with the existing code.

| Milestone | What you work on | What you should be able to explain |
|---|---|---|
| [M0 — PyTorch basics](Learning/M0.md) | Learn `y = 2x + 1` | How inputs, loss, gradients, and parameter updates connect |
| [M1 — Differentiable simulator](Learning/M1.md) | Simulate pendulum motion | How one physics step becomes a batch of trajectories |
| [M2 — System identification](Learning/M2.md) | Fit length and damping | How measured motion helps us adjust the simulator |
| [M3 — Controller training](Learning/M3.md) | Train two controllers | How a network learns to choose torque without correct-torque labels |
| [M4 — Reference evaluation](Learning/M4.md) | Compare both controllers | What the measured errors show and what they cannot prove |

While working through the assignments, treat `real_robot.py` as a black box. Use its public functions to collect data and evaluate your controller rather than reading its hidden parameter values.

I have kept my original [worklog](WORKLOG.md), including the parts I misunderstood and the corrections I received. Read it alongside your own attempts if it helps you connect the ideas.
