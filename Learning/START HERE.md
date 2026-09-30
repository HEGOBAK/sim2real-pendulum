# Start here — your Sim2Real Pendulum project

Your working folder is **Desktop → Projects → sim2real-pendulum**.
Everything you need to begin is here. All milestones are still yours to complete.

## First, get oriented

1. Open **Sim2Real Guide → Open Project.command** to launch this folder in VS Code.
2. Watch [the walkthrough](../Sim2Real%20Guide/pendulum-walkthrough.mp4), or read [its transcript](../Sim2Real%20Guide/walkthrough-transcript.md).
3. Read [README.md](../README.md) for the exercise instructions. Use [WORKLOG.md](../WORKLOG.md) for your own learning notes.

The guide's ZIP and **Original Desktop Starter** are untouched backups. Write code in the project root, one folder above Learning. This folder contains instructions only. Backup tests are excluded from normal test discovery.

## Learn one milestone at a time

Begin with [M0 — PyTorch basics](M0.md). The later files are placeholders, not assigned work. After finishing M0, ask for a review and explicitly request the M1 guide. We will prepare each later guide only when you ask.

| Guide | Instruction status |
|---|---|
| [M0](M0.md) | Ready to begin; your learning is not marked complete |
| [M1](M1.md) | Waiting for your request |
| [M2](M2.md) | Waiting for your request |
| [M3](M3.md) | Waiting for your request |
| [M4](M4.md) | Waiting for your request |
| [M5](M5.md) | Waiting for your request |

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

## Your personal learning assistant

Use the same chat where we set up this project. Ask naturally, as you would ask a tutor. You do not need another app or an API setup. Write and run your practice code in VS Code; use the chat for explanations, hints, review, and questions.

A useful message to start a session:

> I am working on Learning/M0.md. Be my tutor. Teach one concept at a time, ask me to predict the result, then let me try. Give hints before answers. Do not edit my exercise files or solve milestone TODOs. Wait for my response before moving on.

When stuck, share the file or small code snippet, the exact error or output, what you expected, and what you have tried. You can ask me to read your saved `m0_practice.py` directly in this project. I do not automatically watch your editor as you type; tell me when you want a review.

Examples:

- “What does tensor shape mean? Use a small example, then ask me a question.”
- “I saved m0_practice.py. Read it and give one hint without changing it.”
- “Here is my output. Help me understand why my prediction was wrong.”
- “Quiz me on M0, one question at a time.”
- “I think I finished M0. Review my work and explanations. If I am ready, prepare M1.md.”

If you start a new chat, provide this project's location, the current milestone file, and your latest WORKLOG notes. Do not assume a new chat already knows your progress. Check explanations against your own runs and the official tutorial.

OpenAI documents answering questions about code as a supported use: [official OpenAI documentation](https://developers.openai.com/api/docs/guides/code-generation). The tutoring routine above is our learning agreement for this project.

## How this starting guide supports the next step

You now know where to read instructions, write code, run Python, and ask for help. Those habits let you begin M0 without mixing up folders or having the assistant do your learning work. Your notes and verified experiments will help us choose the right pace for the next milestone.
