import csv
from pathlib import Path

import matplotlib.pyplot as plt
import torch

from calibrate import calibrate
from policy import train_policy
from real_robot import run_policy_on_real


def mean_holding_error(errors):
    # Validate absolute angle errors and average the last 100 steps.
    if errors.ndim != 2 or errors.shape[0] == 0 or errors.shape[1] < 100:
        raise ValueError("Expected errors shaped (n, T), with n > 0 and T >= 100.")
    if not torch.isfinite(errors).all():
        raise ValueError("Evaluation errors contain NaN or infinity.")
    if (errors < 0).any():
        raise ValueError("Expected nonnegative absolute angle errors.")
    return errors[:, -100:].mean().item()


def error_reduction(nominal_error, calibrated_error):
    # Return reduction in radians and percent; percent is undefined at zero.
    absolute = nominal_error - calibrated_error
    relative = None if nominal_error == 0 else 100 * absolute / nominal_error
    return absolute, relative


if __name__ == "__main__":
    # Define settings once so training calls and saved metadata agree.
    training_seed = 1
    evaluation_seed = 123
    training_iterations = 300
    learning_rate = 0.01
    project_root = Path(__file__).resolve().parent

    L_cal, b_cal, _ = calibrate()
    p_nom = train_policy(torch.tensor(1.0), torch.tensor(0.1),
                         iters=training_iterations, lr=learning_rate, seed=training_seed)
    p_cal = train_policy(torch.tensor(L_cal), torch.tensor(b_cal),
                         iters=training_iterations, lr=learning_rate, seed=training_seed)

    rows = []
    controllers = [("nominal sim", p_nom), ("calibrated sim", p_cal)]
    for name, p in controllers:
        p.eval()
        torch.manual_seed(evaluation_seed)
        with torch.no_grad():
            errors = run_policy_on_real(p)  # Absolute angle errors, shape (n, T).

        err = mean_holding_error(errors)
        print(f"{name:15s} shape={tuple(errors.shape)}, last-100 mean |error|: {err:.6f} rad")
        rows.append({
            "Controller": name,
            "L": p.L,
            "b": p.b,
            "mean_abs_error_rad": err,
            "training_seed": training_seed,
            "evaluation_seed": evaluation_seed,
            "training_iterations": training_iterations,
            "learning_rate": learning_rate,
            "num_trajectories": errors.shape[0],
            "num_steps": errors.shape[1],
        })

    # Write only after both evaluations pass, keeping both rows in one file.
    results_dir = project_root / "results"
    results_dir.mkdir(exist_ok=True)
    with (results_dir / "m4_comparison.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    abs_reduction, rel_reduction = error_reduction(rows[0]["mean_abs_error_rad"], rows[1]["mean_abs_error_rad"])
    print(f"Absolute reduction: {abs_reduction:.6f} rad")
    if rel_reduction is None:
        print("Relative reduction: undefined (nominal error is zero)")
    else:
        print(f"Relative reduction: {rel_reduction:.2f}%")

    # Preserve M3's training comparison; it is separate from reference error.
    figures_dir = project_root / "figures"
    figures_dir.mkdir(exist_ok=True)
    plt.figure()
    for name, p in controllers:
        plt.plot(p.cost_history, label=name)
    plt.xlabel("Update number")
    plt.ylabel("Training cost")
    plt.title("Controller training")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "m3_training_comparison.png")
    plt.close()
