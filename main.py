from neural_network.preprocess import (
    tokenize_sentences,
    build_vocab,
    convert_to_vectors,
    normalize_vectors,
)
from neural_network.train import train
from neural_network.predict import predict
from genetic_algorithm.ga import genetic_algorithm, initialize_population
from genetic_algorithm.art import visualize_artwork
import numpy as np


def setup_and_train_nn():
    """Setup and train the neural network"""
    # Training data
    sentences = [
        "I hate myself, I wish I was never born. Life is meaningless",
        "Life sucks, I wish I was never born",
        "There is no hope for tomorrow",
        "Everything is pointless and we all die alone",
        "Nothing matters in this empty universe",
        "Why try when everything ends in darkness",
        "Life is just suffering without purpose",
        "I love when it rains",
        "Happiness is the key to life",
        "Love and peace make life worth living",
        "Accept what you cannot change, focus on what you can",
        "Find peace in the present moment",
        "Wisdom comes from accepting life's challenges",
        "Virtue is the only true good",
        "Inner peace comes from within, not external circumstances",
        "Face adversity with courage and wisdom",
    ]
    labels = [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]  # 1 for Nihilistic, 0 for Stoic

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
    return vocab, W1, b1, W2, b2


def analyze_text_and_generate_art(text, vocab, W1, b1, W2, b2):
    """Analyze text and generate corresponding artwork"""
    X = convert_to_vectors([text], vocab)
    X = normalize_vectors(X)

    prediction = predict(X, W1, b1, W2, b2)
    nihilistic_score = float(prediction[0])
    stoic_score = 1 - nihilistic_score

    scores = {"stoic": stoic_score, "nihilistic": nihilistic_score}

    print(f"\nText Analysis Results:")
    print(f"Stoic Score: {scores['stoic']:.2%}")
    print(f"Nihilistic Score: {scores['nihilistic']:.2%}")

    population_size = 100
    generations = 10
    population = initialize_population(population_size, scores)

    best_artwork = genetic_algorithm(population, scores, generations)

    output_filename = "generated_artwork.png"
    visualize_artwork(best_artwork, output_filename)

    return best_artwork


def main():
    print("Initializing and training neural network...")
    vocab, W1, b1, W2, b2 = setup_and_train_nn()

    while True:
        print("\nEnter a philosophical text to generate art (or 'quit' to exit):")
        text = input("> ")

        if text.lower() == "quit":
            break

        print("\nAnalyzing text and generating artwork...")
        best_artwork = analyze_text_and_generate_art(text, vocab, W1, b1, W2, b2)
        print("\nArtwork generated! Check 'generated_artwork.png'")


if __name__ == "__main__":
    main()
