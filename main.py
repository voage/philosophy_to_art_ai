from neural_network.preprocess import (
    tokenize_sentences,
    build_vocab,
    convert_to_vectors,
    normalize_vectors,
)
from neural_network.train import train
from neural_network.predict import predict
from genetic_algorithm.ga import genetic_algorithm
from genetic_algorithm.artwork_generator import initialize_population
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
        "Existence is an endless cycle of pain",
        "We're all just dust in a meaningless void",
        "There's no point in trying anymore",
        "Every effort leads to inevitable failure",
        "The universe is cold and indifferent",
        "All achievements are ultimately worthless",
        "Happiness is just a temporary illusion",
        "We're trapped in a meaningless existence",
        "Life is a cruel joke without a punchline",
        "Nothing we do will ever matter",
        "All paths lead to the same emptiness",
        "Hope is a lie we tell ourselves",
        "The world is devoid of meaning or purpose",
        "Every joy is followed by deeper sorrow",
        "We're all alone in our suffering",
        "Time erases everything we build",
        "Life is an exercise in futility",
        "There's no escape from the void",
        "Everything good eventually turns to ash",
        "We're just specks in an uncaring cosmos",
        "All relationships end in pain",
        "Truth is there is no truth",
        "Life is a prison of consciousness",
        "Nothing is worth the struggle",
        "We're born to suffer and die",
        "All hope leads to disappointment",
        "The future holds only darkness",
        "Existence is a burden",
        "Love is temporary, pain is forever",
        "We're all walking towards oblivion",
        "Nothing truly matters in the end",
        "Life is an endless series of losses",
        "All efforts are ultimately futile",
        "The universe cares nothing for us",
        "Every dream ends in awakening",
        "We're trapped in endless suffering",
        "Nothing lasts, everything fades",
        "Life is a meaningless struggle",
        "All joy is fleeting and hollow",
        "We're destined for nothingness",
        "Purpose is an illusion",
        "Everything ends in darkness",
        "The void awaits us all",
        "I love when it rains",
        "Happiness is the key to life",
        "Love and peace make life worth living",
        "Accept what you cannot change, focus on what you can",
        "Find peace in the present moment",
        "Wisdom comes from accepting life's challenges",
        "Virtue is the only true good",
        "Inner peace comes from within, not external circumstances",
        "Face adversity with courage and wisdom",
        "Every obstacle is an opportunity to grow",
        "True strength lies in self-control",
        "Focus on what you can influence",
        "Embrace the present moment fully",
        "Character is destiny",
        "Live according to nature",
        "Wisdom comes through experience",
        "Control your reactions, not events",
        "Find joy in simple things",
        "Practice gratitude daily",
        "Accept change as natural",
        "Live with purpose and integrity",
        "Cultivate inner tranquility",
        "Choose virtue over pleasure",
        "Find strength in adversity",
        "Be the master of your thoughts",
        "Act with reason and wisdom",
        "Embrace life's challenges",
        "Seek understanding, not judgment",
        "Practice mindful living",
        "Find peace in simplicity",
        "Choose your responses wisely",
        "Build character through actions",
        "Accept reality as it is",
        "Find meaning in duty",
        "Cultivate emotional resilience",
        "Live with noble purpose",
        "Seek wisdom through reflection",
        "Practice self-discipline",
        "Find strength in principles",
        "Choose courage over comfort",
        "Act with justice and mercy",
        "Embrace natural law",
        "Seek truth in all things",
        "Find beauty in wisdom",
        "Practice rational thinking",
        "Live with authenticity",
        "Choose virtue over vice",
        "Build inner strength",
        "Accept life's seasons",
        "Find peace in wisdom",
    ]
    labels = [0] * 50 + [1] * 50  # 50 Nihilistic (0), 50 Stoic (1)

    tokenized_sentences = tokenize_sentences(sentences)
    vocab = build_vocab(tokenized_sentences)
    X = convert_to_vectors(sentences, vocab)
    X = normalize_vectors(X)
    Y = np.array(labels).reshape(-1, 1)

    input_size = X.shape[1]
    hidden_size = 16
    epochs = 1000
    learning_rate = 1

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
        analyze_text_and_generate_art(text, vocab, W1, b1, W2, b2)
        print("\nArtwork generated! Check 'generated_artwork.png'")


if __name__ == "__main__":
    main()
