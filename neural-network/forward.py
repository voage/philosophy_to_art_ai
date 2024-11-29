import numpy as np

def sigmoid(Z):
    return 1 / (1 + np.exp(-Z))

def relu(Z):
    return np.maximum(0, Z)

def forward_propagation(X, W1, b1, W2, b2):
    """
    Perform forward propagation through the network.

    Args:
        X: Input data 
        W1, b1: Weights and biases for the hidden layer.
        W2, b2: Weights and biases for the output layer.

    Returns:
        Z1, A1: Intermediate activations from the hidden layer.
        Z2, A2: Final output from the output layer.
    """
    # Hidden layer
    Z1 = np.dot(X, W1) + b1
    A1 = relu(Z1)

    # Output layer
    Z2 = np.dot(A1, W2) + b2
    A2 = sigmoid(Z2)

    return Z1, A1, Z2, A2
