import math, torch
from real_robot import collect_real_data
from sim import rollout

def calibrate(iters=400, lr=0.05):
    th0, om0, U, Y = collect_real_data()
    # TODO(M2): make log L and log b trainable (start at log 1.0 and log 0.1),
    # optimize MSE(rollout(...), Y) with Adam, record the loss history.
    raise NotImplementedError   # return L_cal, b_cal, loss_history

if __name__ == "__main__":
    L, b, hist = calibrate()
    print(f"calibrated L={L:.3f}  b={b:.3f}  final loss={hist[-1]:.5f}")
