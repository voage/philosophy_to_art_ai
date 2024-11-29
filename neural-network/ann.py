from preprocess import preprocess_text

text = input('Enter some text: ')
words = preprocess_text(text)
print(words)