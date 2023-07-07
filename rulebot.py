import numpy as np
import nltk
import string
import random
from flask import Flask, render_template, request, jsonify
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

f = open('data.txt', 'r', errors='ignore')
raw_doc = f.read()
raw_doc = raw_doc.lower()

nltk.download('punkt')
nltk.download('wordnet')

sentence_tokens = nltk.sent_tokenize(raw_doc)
word_tokens = nltk.word_tokenize(raw_doc)

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

def LemNormalize(text):
    tokens = nltk.word_tokenize(text.lower().translate(remove_punc_dict))
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]
    return stemmed_tokens

remove_punc_dict = dict((ord(punct), None) for punct in string.punctuation)

greet_inputs = ('hello', 'hi', 'hai', 'whassup', 'how are you','hey')
greet_responses = ('Hi', 'Hey', 'Hey there')

def greet(sentence):
    for word in sentence.split():
        if word.lower() in greet_inputs:
            return random.choice(greet_responses)

def get_response(user_response):
    robo1_response = ''
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sentence_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if req_tfidf == 0:
        robo1_response = robo1_response + "I am sorry. I am unable to understand you!"
        return robo1_response
    else:
        robo1_response = robo1_response + sentence_tokens[idx]
        return robo1_response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process-user-input", methods=["POST"])
def process_user_input():
    data = request.get_json()
    user_input = data['message']
    user_input = user_input.lower()
    
    if user_input != 'bye': 
        if user_input == 'thank you' or user_input == 'thanks':
            return jsonify({'message': "You're welcome!"})
        else:
            if greet(user_input) is not None:
                return jsonify({'message': greet(user_input)})
            else:
                sentence_tokens.append(user_input)
                word_tokens.extend(nltk.word_tokenize(user_input))
                final_words = list(set(word_tokens))
                response = get_response(user_input)
                sentence_tokens.remove(user_input)
                return jsonify({'message': response})
    else:
        return jsonify({'message': "Goodbye!"})

if __name__ == "__main__":
    app.run()