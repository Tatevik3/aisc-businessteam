import pandas as pd
import random
from sentence_transformers import SentenceTransformer, util


df = pd.read_excel("tariff_database_2025.xlsx")

# sentences hold the row of information
# exel_row holds the index of the row in the excel file
sentences = []
exel_row = []  

# itterates through the excel and creates a sentence for each row
for i, row in df.iterrows():
    sentence = (
        f" \nProduct description: {row['brief_description']}\n"
        f"Tariff rate: {row['mfn_text_rate']}\n"
        f"Date effective: {row['begin_effect_date']}"
    )
       
    sentences.append(sentence)
    exel_row.append(i)

# the pretrained language model used to encode the sentences
model = SentenceTransformer('all-MiniLM-L6-v2')
sentence_embeddings = model.encode(sentences, convert_to_tensor=True)

# list of greetings user can input and greetings the bot can respond with
greeting_inputs = ("hello", "hi", "hey", "greetings", "yo, what's up", "howdy", "hi there", "good day", "good morning", "good afternoon", "good evening")
greeting_responses = ["Hi!", "Hello there!", "Hey, how can I help you?", "Greetings!", "Hello! What can I assist you with today?", "Hi! How can I help you?"]

# checks if the user input is a greeting and returns a response
def generate_greeting_response(msg):
    for word in msg.lower().split():
        if word in greeting_inputs:
            return random.choice(greeting_responses)

# checks if greeting, if it is returns a greeting 
# otherwise computes cosine similarity and returns the best match of product
# if no match is found, returns a default message
def generate_response(user_input):
    greeting = generate_greeting_response(user_input)
    if greeting:
        return greeting
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(user_embedding, sentence_embeddings)[0]

    best_idx = similarities.argmax().item()
    best_score = similarities[best_idx].item()
    if best_score < 0.5:
        return "I'm not sure I understand. Try asking for [product] tariff rate."
    
    return sentences[best_idx]