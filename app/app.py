from flask import Flask, render_template, request, jsonify
import bot2  

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['message'].lower()
    
    greeting = bot2.generate_greeting_response(user_message)
    if greeting:
        reply = greeting
    else:
        reply = bot2.generate_response(user_message)
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
