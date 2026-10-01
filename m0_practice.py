import torch

# -- 1. Create the training data --

x = torch.tensor([[-2.],[-1.],[0.],[1.],[2.]])
y = torch.tensor([[-3.],[-1.],[1.],[3.],[5.]])

# print(x.shape)
# print(y.shape)


# -- 2. Do not need custom class - One layer is enough --

model = torch.nn.Linear(1, 1) # One input/output per example
pred = model(x) # Applies to every input

# print(pred)
# print(pred.shape)


# -- 3. Measure how wrong those predictions are --

loss_fn = torch.nn.MSELoss()
loss = loss_fn(pred, y) # A tensor with avg loss score and ready for backprop

# print("Initial loss:", loss.item())


# -- 4. Optimizer and one learning update --

learning_rate = 0.05 # Set learning rate
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate) # Gives SGD w & b

# optimizer.zero_grad() # Clears prev gradients because gradients accumulate
# loss.backward() # Calc new gradient

# print("Weight gradient:", model.weight.grad)
# print("Bias gradient:", model.bias.grad)

# optimizer.step() # Updates w & b from new gradient

# # Fresh loss after one update
# new_pred = model(x)
# new_loss = loss_fn(new_pred, y)
# print("Loss after one update:", new_loss.item())


# -- 5. Repeat 300 times --

for i in range(300):
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()

	pred = model(x)
	loss = loss_fn(pred, y)

# print("Loss after 300 update:", loss.item())


# -- 6. Test --

print("Learned weight:", model.weight.item())
print("Learned bias:", model.bias.item())

test_x = torch.tensor([[3.], [4.]])

with torch.no_grad(): # Disable gradient tracking
    test_pred = model(test_x)

print("New predictions:", test_pred)

