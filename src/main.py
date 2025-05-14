import nltk
import numpy as np
import string
import bs4 as bs
import urllib.request
import re
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

link = urllib.request.urlopen("https://en.wikipedia.org/wiki/Tariffs_in_the_second_Trump_administration")
link = link.read()
data = bs.BeautifulSoup(link, "lxml")
data_paragraphs = data.find_all("p")
data_text = ""
for para in data_paragraphs:
    data_text+=para.text
data_text = data_text.lower()
data_text= re.sub(r'\[[0-9]*\]', ' ', data_text)
data_text= re.sub(r'\s+', ' ', data_text)

sen=nltk.sent_tokenize(data_text)
words = nltk.word_tokenize(data_text)

wnlem=nltk.stem.WordNetLemmatizer()
def perform_lemm(tokens):
    return[wnlem.lemmatize(token) for token in tokens]
pr = dict((ord(punctuation), None) for punctuation in string.punctuation)
def get_processed_text(document):
    return perform_lemm(nltk.word_tokenize(document.lower().translate(pr)))
greeting_inputs = ("hey", "hello", "sup", "yo")
greeting_responses = ["Hello", "Hello, how are you?"]

def generate_greeting_response(greeting):
    for token in greeting.split():
        if token.lower() in greeting_inputs:
            return random.choice(greeting_responses)
        
def generate_response(user_response):
    bot_response = " "
    sen.append(user_response)
    word_vectorizer = TfidfVectorizer(tokenizer=get_processed_text, stop_words='english')
    word_vectors=  word_vectorizer.fit_transform(sen)

    similar_vector_values=cosine_similarity(word_vectors[-1], word_vectors)
    similar_sentence_number= similar_vector_values.argsort()[0][-2]

    matched_vector=similar_vector_values.flatten()
    matched_vector.sort()
    vector_matched = matched_vector[-2]

    if vector_matched == 0:
        bot_response = bot_response + "I'm sorry, I dont understand:("
        return bot_response
    else:
        bot_response = bot_response +sen[similar_sentence_number]
        return bot_response
continue_flag= True
print("Hello, I am the tarrif master, shoot me a question if you dare")
while(continue_flag==True):
    human = input()
    human = human.lower()
    if human!="bye":
        if human == "thanks" or human == "thank you":
            continue_flag = False
            print("You are most welcome")
        else:
            if generate_greeting_response(human)is not None:
                print("Tarrif king:"+ generate_greeting_response(human))
            else:
                print("Tarrif King:", end="")
                print(generate_response(human))
                sen.remove(human)
    else:
        continue_flag = False
        print("Tarrif master out")
        