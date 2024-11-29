import string

def to_lowercase(text):
    return text.lower()

def remove_punctuation(text):
    return ''.join(char for char in text if char not in string.punctuation)

def tokenize(text):
    return text.split()

def remove_stopwords(words):
    stopwords = {'the', 'is', 'in', 'and', 'to', 'a', 'of', 'this', 'how', 'an'}  
    return [word for word in words if word not in stopwords]

def preprocess_text(text):
    text = to_lowercase(text)
    text = remove_punctuation(text)
    words = tokenize(text)
    words = remove_stopwords(words)
    return words

