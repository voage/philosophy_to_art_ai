import numpy as np
from preprocess import tokenize_sentences, build_vocab, convert_to_vectors, normalize_vectors
from train import train
from predict import predict

# 1. Input: 100 sentences
sentences = [
    "I hate myself, I wish I was never born. Life is meaningless",  # Nihilistic -> 1
    "Life sucks, I wish I was never born",                         # Nihilistic -> 1
    "I love when it rains"                                         # Stoic -> 0
]
labels = [1, 1, 0]  # Make sure these match the intent of the sentences


# 2. Tokenize and process sentences
tokenized_sentences = tokenize_sentences(sentences)         # Tokenize sentences
vocab = build_vocab(tokenized_sentences)                    # Build vocabulary
X = convert_to_vectors(sentences, vocab)                   # Convert sentences to vectors
X = normalize_vectors(X)                                   # Normalize vectors

# Convert labels to a numpy array
Y = np.array(labels).reshape(-1, 1)

# 3. Training parameters
input_size = X.shape[1]  # Vocabulary size
hidden_size = 16         # Hidden layer size
epochs = 1000            # Number of training epochs
learning_rate = 0.01     # Learning rate

# 4. Train the model
W1, b1, W2, b2 = train(X, Y, input_size, hidden_size, epochs, learning_rate)

# 5. Predict on the same dataset (or a test set)
predictions = predict(X, W1, b1, W2, b2)
print("Predictions:", predictions)
