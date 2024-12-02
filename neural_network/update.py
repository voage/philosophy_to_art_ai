def update_parameters(W1, b1, W2, b2, dW1, db1, dW2, db2, learning_rate, lambda_reg=0.01):
    """
    Update the weights and biases using gradient descent.

    Args:
        W1, b1: Weights and biases for the hidden layer.
        W2, b2: Weights and biases for the output layer.
        dW1, db1, dW2, db2: Gradients for the weights and biases.
        learning_rate: Scalar value for the learning rate.

    Returns:
        Updated weights and biases.
    """
    dW1 += lambda_reg * W1
    dW2 += lambda_reg * W2

    W1 -= learning_rate * dW1
    b1 -= learning_rate * db1
    W2 -= learning_rate * dW2
    b2 -= learning_rate * db2
    return W1, b1, W2, b2
