import numpy as np
from collections import Counter

def tokenize_sentences(sentences):
    """
    Tokenize sentences into a list of words.
    """
    return [sentence.lower().split() for sentence in sentences]

def build_vocab(tokenized_sentences):
    """
    Build a vocabulary from tokenized sentences.
    """
    vocab = {word: i for i, word in enumerate(set(word for sentence in tokenized_sentences for word in sentence))}
    return vocab

def sentence_to_bow(sentence, vocab):
    """
    Convert a single sentence to a Bag-of-Words vector.
    """
    bow = np.zeros(len(vocab))
    word_counts = Counter(sentence.lower().split())
    for word, count in word_counts.items():
        if word in vocab:
            bow[vocab[word]] = count
    return bow

def convert_to_vectors(sentences, vocab):
    """
    Convert all sentences to Bag-of-Words vectors.
    """
    return np.array([sentence_to_bow(sentence, vocab) for sentence in sentences])

def normalize_vectors(X):
    """
    Normalize vectors to scale features between 0 and 1.
    """
    return X / np.max(X, axis=0)
