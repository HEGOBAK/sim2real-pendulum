import math, torch
from real_robot import collect_real_data
from sim import rollout
# For the plot (loss history) (./figures/m2_calibration_loss.png)
from pathlib import Path
import matplotlib.pyplot as plt

def calibrate(iters=400, lr=0.05):
    th0, om0, U, Y = collect_real_data()
    # TODO(M2): make log L and log b trainable (start at log 1.0 and log 0.1),
    # optimize MSE(rollout(...), Y) with Adam, record the loss history.

    # -- We know --
    # th0, om0: starting angles and angular velocities of the real robot
    # U: control inputs applied to the real robot
    # Y: angles measured from the real robot after applying U starting from th0, om
    # th0, om0, U, Y are all torch tensors
    # th0, om0 shape [n]; U, Y shape [n, T]
    # rollout(th0, om0, U, L, b) returns shape [n, T] (angles)
    # MSE loss: torch.nn.functional.mse_loss(pred, target)

    # print(f"Printing shapes of the data collected from the real robot:")
    # print(f"Starting angles:     {th0.shape}")
    # print(f"Starting velocities: {om0.shape}")
    # print(f"Torque inputs:       {U.shape}")
    # print(f"Measured angles:     {Y.shape}")

    # -- 1. Initialize log L and log b as trainable parameters --
    log_L = torch.tensor(math.log(1.0), requires_grad=True) # exp(log(1.0)) = 1.0
    log_b = torch.tensor(math.log(0.1), requires_grad=True) # exp(log(0.1)) = 0.1
    optimizer = torch.optim.Adam([log_L, log_b], lr=lr) # Adam optimizer for log L and log b

    loss_history = [] # To record the loss at each iteration

    for i in range(iters):
        # 1. Zero the gradients of the optimizer
        # 2. Compute the predictions using rollout()
        # 3. Compute the loss using MSE
        # 4. Backpropagate the loss
        # 5. Step the optimizer

        L = torch.exp(log_L) # Convert log L back to L
        b = torch.exp(log_b) # Convert log b back to b

        optimizer.zero_grad()
        pred = rollout(th0, om0, U, L, b)

        # pred - Y has shape (n, T); loss has shape ()
        # loss = (pred - Y).square().mean() 
        loss = torch.nn.functional.mse_loss(pred, Y) # alternative way to compute MSE
        loss_history.append(loss.item())
       
        loss.backward()
        optimizer.step()

    # Final calibrated values and final loss
    with torch.no_grad(): # No need to track gradients for final values
        L_cal = torch.exp(log_L).item() # Final calibrated L
        b_cal = torch.exp(log_b).item() # Final calibrated b

        pred_final = rollout(th0, om0, U, L_cal, b_cal)
        loss_final = (pred_final - Y).square().mean().item()
        loss_history.append(loss_final) # Append final loss to history

    return (L_cal, b_cal, loss_history)   # return L_cal, b_cal, loss_history


if __name__ == "__main__":
    L, b, hist = calibrate()
    # print(f"calibrated L={L:.3f}  b={b:.3f}  final loss={hist[-1]:.5f}")

    # Initial loss, final loss, and fitted values
    print(f"Initial loss: {hist[0]:.5f}")
    print(f"Final loss: {hist[-1]:.5f}")
    print(f"Estimated length:  {L:.4f}")
    print(f"Estimated damping: {b:.4f}")

    # Plot the loss history (./figures/m2_calibration_loss.png)
    Path("figures").mkdir(exist_ok=True)
    plt.plot(hist)
    plt.xlabel("Update number")
    plt.ylabel("Mean squared error")
    plt.title("Pendulum calibration")
    plt.tight_layout()
    plt.savefig("figures/m2_calibration_loss.png")
    plt.close()