import torch
from sim import step
TARGET, UMAX = 0.6, 10.0

def make_policy():
    return torch.nn.Sequential(torch.nn.Linear(2, 32), torch.nn.Tanh(), torch.nn.Linear(32, 1))

def train_policy(L, b, iters=300, lr=0.01, seed=1):
    """Train by backpropagating the task cost through the differentiable simulator."""
    torch.manual_seed(seed)
    policy = make_policy()
    # TODO(M3): each iteration - sample a batch of start angles near 0,
    # roll out ~150 steps with u = UMAX*tanh(policy([th-TARGET, om])),
    # cost = mean((th-TARGET)^2) + 0.01*mean(om^2) over time; backprop; Adam step.
        
    optimizer = torch.optim.Adam(policy.parameters(), lr=lr) # Adam optimizer for policy parameters
    cost_history = [] # To record the cost at each iteration

    for i in range(iters):
        # Sample a batch of starting angles and angular velocities
        n = 32 # Batch size
        th = torch.rand(n) * 0.2 - 0.1 # Starting angles near 0 varying between -0.1 and 0.1 radians
        om = torch.zeros(n)  # Starting angular velocities at 0

        T = 150 # Number of time steps
        cost = [] # List to accumulate cost at each time step

        # Loop over time steps to simulate the system and compute the cost
        for t in range(T):
            u = (UMAX * torch.tanh(policy(torch.stack([th - TARGET, om], dim=1)))).squeeze(-1) # Control input based on policy output
            th, om = step(th, om, u, L, b) # Update angle and angular velocity

            # Compute the cost as the mean squared error of the angle from the target and a small penalty on angular velocity
            cost.append((((th - TARGET)**2)).mean() + (0.01 * (om**2)).mean())


        cost = torch.stack(cost).mean() # Average cost over time steps
        cost_history.append(cost.item()) # Record the cost for this iteration
        # if i % 50 == 0: # Print the cost every 50 iterations for monitoring
        #     print(f"Iteration {i}: cost = {cost.item():.4f}")


        optimizer.zero_grad() # Clear previous gradients
        cost.backward() # Backpropagate the cost to compute gradients
        optimizer.step() # Update policy parameters based on gradients

    # Store the cost history and other relevant information in the policy object for later analysis
    policy.cost_history = cost_history # Store the cost history in the policy for later analysis
    policy.L = L.item() # Store the value of L in the policy for reference
    policy.b = b.item() # Store the value of b in the policy for reference
    policy.seed = seed # Store the random seed used for training in the policy for reference

    return policy

