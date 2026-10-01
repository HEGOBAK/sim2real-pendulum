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
Status: Not started

## M2 — System Identification
Status: Not started

## M3 — Controller Training
Status: Not started

## M4 — Real-Pendulum Evaluation
Status: Not started

## M5 — Results & README
Status: Not started
