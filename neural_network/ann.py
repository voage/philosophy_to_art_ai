import numpy as np
from preprocess import tokenize_sentences, build_vocab, convert_to_vectors, normalize_vectors
from train import train
from predict import predict

# 1. Training Data (labeled sentences)
sentences = [
    "I hate myself, I wish I was never born. Life is meaningless",  # Nihilistic -> 1
    "Life sucks, I wish I was never born",                         # Nihilistic -> 1
    "I love when it rains",                                        # Stoic -> 0
    "Happiness is the key to life",                                # Stoic -> 0
    "There is no hope for tomorrow",                               # Nihilistic -> 1
    "Love and peace make life worth living"                        # Stoic -> 0
]
labels = [1, 1, 0, 0, 1, 0]  # Corresponding labels

# 2. Tokenize and process training data
tokenized_sentences = tokenize_sentences(sentences)         # Tokenize sentences
vocab = build_vocab(tokenized_sentences)                    # Build vocabulary
X = convert_to_vectors(sentences, vocab)                   # Convert sentences to vectors
X = normalize_vectors(X)                                   # Normalize vectors

# Convert labels to numpy array
Y = np.array(labels).reshape(-1, 1)

# 3. Training parameters
input_size = X.shape[1]  # Vocabulary size
hidden_size = 16         # Hidden layer size
epochs = 1000            # Number of training epochs
learning_rate = 0.005 # Lower learning rate

# 4. Train the model
W1, b1, W2, b2 = train(X, Y, input_size, hidden_size, epochs, learning_rate)

# 5. Predict on new sentences (unlabeled)
new_sentences = [
    "I feel lost and hopeless in this world",             # Expected: Nihilistic
    "Gratitude makes life beautiful",                    # Expected: Stoic
    "I hate everything about myself and my existence"    # Expected: Nihilistic
]

# Process new sentences using the same tokenizer and vocab
new_X = convert_to_vectors(sentences, vocab)         # Convert new sentences to vectors
new_X = normalize_vectors(new_X)                        # Normalize new data

# Make predictions
predictions = predict(new_X, W1, b1, W2, b2)
print(predictions)

# Interpret predictions
for sentence, prob in zip(new_sentences, predictions.flatten()):
    stoic_score = (1 - prob) * 100  # Probability of being Stoic
    nihilistic_score = prob * 100   # Probability of being Nihilistic
    print(f"'{sentence}' -> Stoic: {stoic_score:.2f}%, Nihilistic: {nihilistic_score:.2f}%")