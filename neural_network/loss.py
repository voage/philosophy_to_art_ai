import numpy as np

def compute_loss(Y, A2):
    """
    Compute the binary cross-entropy loss.

    Args:
        Y: True labels (m x 1).
        A2: Predicted probabilities (m x 1).

    Returns:
        Loss: Scalar value representing the loss.
    """
    m = Y.shape[0]
    loss = -np.mean(Y * np.log(A2) + (1 - Y) * np.log(1 - A2))
    return loss
