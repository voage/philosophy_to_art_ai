import string

def to_lowercase(text):
    return text.lower()

def remove_punctuation(text):
    return ''.join(char for char in text if char not in string.punctuation)

def tokenize(text):
    return text.split()

def remove_stopwords(words, stopwords):
    return [word for word in words if word not in stopwords]

def stem_word(word):
    if word.endswith(('ing', 'ed', 'es', 's')) and len(word) > 4:  
        return word[:-1]
    return word

def stem_words(words):
    return [stem_word(word) for word in words]

def preprocess_text_modular(text):
    stopwords = {'the', 'is', 'in', 'and', 'to', 'a', 'of', 'this', 'how', 'an'}  
    
    text = to_lowercase(text)
    text = remove_punctuation(text)
    words = tokenize(text)
    words = remove_stopwords(words, stopwords)
    words = stem_words(words)
    
    return words

text = "This is an example sentence, showing how to preprocess text effectively."
meaningful_words = preprocess_text_modular(text)
print(meaningful_words)
