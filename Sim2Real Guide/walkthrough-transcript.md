# Your pendulum project — walkthrough transcript

Working folder: `/Users/master/Desktop/Projects/sim2real-pendulum`

Private repository: https://github.com/HEGOBAK/sim2real-pendulum

All animated motion is illustrative; no experimental results are shown.

## 00:00 — Your project, from start to finish

You are building a small experiment, not a full robot. The question is: does a controller work better when its simulator has been calibrated using observations from another system? Each milestone gives you one piece of evidence. This animation explains the plan. Its motion is illustrative, not an experimental result.

## 00:21 — 01  Where your work lives

Everything starts on your Desktop. Open Projects, then sim2real pendulum. This is your working project. Start with START HERE dot m d. The Sim2Real Guide folder inside it contains this video, the transcript, tutorial and GitHub shortcuts, and your starter backups. Double click Open Project inside the guide to open the whole project in VS Code. Write code in the project root, not in the backup folder.

## 00:49 — 02  How the tools connect

VS Code is the editor, not a separate place where your project lives. Saving changes updates files in the working folder. Its terminal runs Python using the dot venv environment, which holds PyTorch and the other dependencies. Git records local checkpoints. GitHub stores the commits you push. Saving a file does not automatically upload it.

## 01:12 — 03  Where to read, write, and record

Read README dot m d for the milestone instructions. Write your implementation in the Python file for that milestone. The existing test sim file checks the simulator. Use the work log to record what you learned and what remains. Later, put figures in figures, and small result tables in results. Ask for explanations when stuck, but keep the exercise implementation yours.

## 01:38 — 04  What “real-to-sim-to-real” means

Here, real robot dot p y is a software stand-in for physical hardware. There is no connected physical robot in this setup. Treat its public functions like a hardware interface, and do not inspect its hidden parameters. Collect observations, adjust your simulator to match them, train a controller in simulation, then evaluate it on the reference system.

## 02:02 — 05  M0 → M1: learn, then simulate

M zero is learning PyTorch: tensors store numbers, autograd tracks derivatives, and optimizers use derivatives to improve adjustable values. Start with the official Learn the Basics tutorial. Then M one builds the pendulum simulator in sim dot p y. Step predicts one time step; rollout combines many steps. The two current test failures are expected because those functions are intentionally unfinished.

## 02:29 — 06  M2: make the simulator fit observations

In M two, use observations returned by the reference system to calibrate the simulator. Calibration means adjusting model parameters so predicted motion matches observed motion. Record how the mismatch, called the loss, changes as you optimize. This turns M one into a model informed by data. Estimate parameters from observations, never from hidden source values.

## 02:54 — 07  M3 → M4: train, then compare

In M three, policy dot p y trains a controller, a function that chooses torque from the current state. Train one using the nominal simulator and another using the calibrated simulator. In M four, evaluate both on the same reference system and compare their late trajectory tracking errors. Better transfer is the hypothesis. The measured outcome is not guaranteed.

## 03:19 — 08  M5: turn work into evidence

M five connects the evidence. Your tested simulator, calibration loss plot, and controller comparison explain what happened. Fill the README with only numbers and figures you actually produced. If calibration does not improve the result, investigate and report that honestly. Keep the repository private while unfinished. A clear, reproducible explanation is the final goal.

## 03:45 — 09  Your next small step

Your next step is only M zero. Open the working folder in VS Code, read the M zero instruction, and try a tiny tensor and gradient experiment as a separate practice exercise. Write down what you understand. For each later session, read one task, make a small change, run a relevant check, and record what happened. Commit meaningful progress locally, then push it to GitHub. Small verified steps become your final experiment.

## Official M0 learning resource

https://pytorch.org/tutorials/beginner/basics/intro.html

## Your normal work cycle

Read README → edit in VS Code → save → run a relevant check → record learning → git add → git commit → git push.

Run commands from the working folder, using its `.venv` interpreter. A commit saves a local checkpoint; push uploads commits. Neither happens merely by saving a file.