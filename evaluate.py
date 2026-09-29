import torch
from calibrate import calibrate
from policy import train_policy
from real_robot import run_policy_on_real

if __name__ == "__main__":
    L_cal, b_cal, _ = calibrate()
    p_nom = train_policy(torch.tensor(1.0), torch.tensor(0.1))
    p_cal = train_policy(torch.tensor(L_cal), torch.tensor(b_cal))
    for name, p in [("nominal sim", p_nom), ("calibrated sim", p_cal)]:
        err = run_policy_on_real(p)[:, -100:].mean().item()
        print(f"{name:15s} steady-state |error| on real robot: {err:.4f} rad")
