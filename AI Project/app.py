from chat import run_chatbot
from flask import Flask, request, render_template
 # Assuming you have a chatbot module

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['user_message']
    
    bot_response = run_chatbot(user_message)
    return bot_response

if __name__ == '__main__':
    app.run(debug=True)
