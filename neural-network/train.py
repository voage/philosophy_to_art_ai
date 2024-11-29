import numpy as np
from forward import forward_propagation
from loss import compute_loss
from backward import backward_propagation
from update import update_parameters

def train(X, Y, input_size, hidden_size, epochs, learning_rate):
    """
    Train the neural network.

    Args:
        X: Input data (m x input_size).
        Y: True labels (m x 1).
        input_size: Number of features in the input.
        hidden_size: Number of neurons in the hidden layer.
        epochs: Number of training iterations.
        learning_rate: Scalar value for learning rate.

    Returns:
        Trained weights and biases (W1, b1, W2, b2).
    """
    np.random.seed(42)

    # Initialize weights and biases
    W1 = np.random.randn(input_size, hidden_size) * 0.01
    b1 = np.zeros((1, hidden_size))
    W2 = np.random.randn(hidden_size, 1) * 0.01
    b2 = np.zeros((1, 1))

    for epoch in range(epochs):
        # Forward propagation
        Z1, A1, Z2, A2 = forward_propagation(X, W1, b1, W2, b2)

        # Compute loss
        loss = compute_loss(Y, A2)

        # Backward propagation
        dW1, db1, dW2, db2 = backward_propagation(X, Y, Z1, A1, A2, W1, W2)

        # Update parameters
        W1, b1, W2, b2 = update_parameters(W1, b1, W2, b2, dW1, db1, dW2, db2, learning_rate)

        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.4f}")

    return W1, b1, W2, b2
