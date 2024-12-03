import numpy as np


def backward_propagation(X, Y, Z1, A1, A2, W1, W2):
    """
    Perform backward propagation to calculate gradients.

    Args:
        X: Input data (m x input_size).
        Y: True labels (m x 1).
        Z1, A1: Hidden layer intermediate values.
        A2: Final output from the output layer.
        W1, W2: Weights for the layers.

    Returns:
        Gradients for W1, b1, W2, b2.
    """
    m = X.shape[0]

    dZ2 = A2 - Y
    dW2 = np.dot(A1.T, dZ2) / m
    db2 = np.sum(dZ2, axis=0, keepdims=True) / m

    dA1 = np.dot(dZ2, W2.T)
    dZ1 = dA1 * (Z1 > 0)
    dW1 = np.dot(X.T, dZ1) / m
    db1 = np.sum(dZ1, axis=0, keepdims=True) / m

    return dW1, db1, dW2, db2
