import numpy as np
from forward import forward_propagation

def predict(X, W1, b1, W2, b2):
    """
    Make predictions using the trained network.

    Args:
        X: Input data (m x input_size).
        W1, b1, W2, b2: Trained weights and biases.

    Returns:
        Predictions (0 for Stoic, 1 for Nihilistic).
    """
    _, _, _, A2 = forward_propagation(X, W1, b1, W2, b2)
    return (A2 >= 0.5).astype(int)
