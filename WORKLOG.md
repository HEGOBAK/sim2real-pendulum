# Sim2Real Pendulum Work Log

---------------------------------------------------------------------------------

## M0 — PyTorch Basics
Status: Completed

Tensor: A block/matrix that we can use to transmit data or perform any acts
Gradient: Derivatives of variables that contributes to the error of the predicted output to the expected output

Linear(input, output)
Number of weights = inputs × outputs
Number of biases  = outputs

MSE (Mean Squared Error):
For each example: (prediction − target)²
Then average the n results and where it will mostly be stored in a "loss" variable
 
Remember to clear gradients every iteration because it accumulates before .backward()

Questions: 
1. Why is x shaped (5, 1) rather than (1, 5)?
-> 5 rows and 1 column means 5 different inputs and each input consist of one information

2. How does loss.backward() connect to optimizer.step()?
-> loss is connected to pred which consist of operation that is done on the input, .backward traces it and by using chain rules, calculate the gradient and store it in model.(w/b).grad which then can be access by optimizer because we passed in model.parameters when initializing it. 

3. What would happen if you removed optimizer.zero_grad()?
-> The gradients would accumulate and will affect the next iteration when we change the w & b which produces the opposite effect.

Assistant comments (corrections):
- A tensor is an array of values; it can have zero, one, two, or more dimensions, not just matrix form.
- A loss gradient measures how the loss changes with respect to each parameter.
- Gradients accumulate when .backward() runs, not before it. Without clearing, old and new gradients mix; this does not necessarily produce the opposite effect.
- Exact syntax: model.weight.grad, model.bias.grad, and model.parameters().

---------------------------------------------------------------------------------

## M1 — Differentiable Simulator
Status: Completed

Rollout is a forward timelapse of step. Each step predicts the next angle and angular velocity given current state and return them so it can be use for the next loop (becoming the next "current state")

Rollout is somewhat like a simulator, it takes in a current state and returns the 'future' states back. You can pass in multiple pendulums at once and it will return the future states for each of them, how many future states depend on the shape of u. 

Doubt: I don't understand how come u is the motor torque of each pendulums at the current state but its shape is [n,t] not just [n] like the angle and velocity of the current state when all of them were initially pass into rollout funciton. Why does it requires time. 

At the end, the rollout returns shape[n, T] similar to u but it stores the angles not the motor torque

Semi-implicit Euler uses updated velocity to calculate next angel not old velocity

Results:
Batch check passed; gradients: tensor(-0.0090) tensor(-0.0119)

Questions: 
1. Why does the angle update use om_next?
-> The next angle depends on the angular velocity at that "time and position" but the angular velocity depends on the angular acceleration at that "time and position" so we must update accordingly in that order

2. What does U[:, t] select?
-> the column at t, basically u in that timestamp of all pendulums

3. Why must the simulator preserve gradient connections to L and b?
-> Because the neural network need to learn from those gradient connections when backpropagating

Assistant comments (corrections):
- Your rollout explanation is correct: each step's output becomes the next step's input. This implementation returns angles only; it updates velocities internally without returning their history.
- Distinguish lowercase u from uppercase U: step receives u with shape (n,), the torque for one time step. rollout receives U with shape (n, T), the full torque schedule for T steps. Starting angles/velocities need only shape (n,) because the simulator computes their future values; motor torques are externally supplied inputs and need to be specified for every step.
- Example: U = [[1, 0, -1], [2, 2, 0]] supplies 3 successive torques for each of 2 pendulums. U[:, 0] gives [1, 2], then U[:, 1] gives [0, 2]. For constant torque, repeat the same value across the row. T is the number of steps, not seconds; duration is T * DT.
- U[:, t] explanation is correct. Capital U is the whole schedule; lowercase u is the selected column.
- For natural motion without a motor push, use U = torch.zeros(1, 50)
- Using om_next is the semi-implicit Euler method we chose, not a requirement of all physics calculations. Acceleration is calculated from the current state, then velocity is updated, then angle uses that new velocity.
- Gradient connections let M2 calculate how trajectory error changes with L and b so an optimizer can fit them; no neural network is needed for M2. In M3, gradients through the simulator will help train the controller network.
- The period and gradient tests and the separate batch check passed in the reviewed run. With these clarifications, the M1 implementation is ready for M2.

---------------------------------------------------------------------------------

## M2 — System Identification
Status: Not started

## M3 — Controller Training
Status: Not started

## M4 — Real-Pendulum Evaluation
Status: Not started

## M5 — Results & README
Status: Not started
