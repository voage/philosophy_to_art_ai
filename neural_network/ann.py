import numpy as np
from preprocess import (
    tokenize_sentences,
    build_vocab,
    convert_to_vectors,
    normalize_vectors,
)
from train import train
from predict import predict

sentences = [
    "I hate myself, I wish I was never born. Life is meaningless",
    "Life sucks, I wish I was never born",
    "I love when it rains",
    "Happiness is the key to life",
    "There is no hope for tomorrow",
    "Love and peace make life worth living",
]
labels = [1, 1, 0, 0, 1, 0]

tokenized_sentences = tokenize_sentences(sentences)
vocab = build_vocab(tokenized_sentences)
X = convert_to_vectors(sentences, vocab)
X = normalize_vectors(X)

Y = np.array(labels).reshape(-1, 1)

input_size = X.shape[1]
hidden_size = 16
epochs = 1000
learning_rate = 0.005

W1, b1, W2, b2 = train(X, Y, input_size, hidden_size, epochs, learning_rate)

new_sentences = [
    "I feel lost and hopeless in this world",
    "Gratitude makes life beautiful",
    "I hate everything about myself and my existence",
]

new_X = convert_to_vectors(new_sentences, vocab)
new_X = normalize_vectors(new_X)

predictions = predict(new_X, W1, b1, W2, b2)
print(predictions)

for sentence, prob in zip(new_sentences, predictions.flatten()):
    stoic_score = (1 - prob) * 100
    nihilistic_score = prob * 100
    print(
        f"'{sentence}' -> Stoic: {stoic_score:.2f}%, Nihilistic: {nihilistic_score:.2f}%"
    )
