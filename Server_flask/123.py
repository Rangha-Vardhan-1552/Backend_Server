from flask import Flask, request, jsonify, Response
import openai
from flask_cors import CORS
import json

# Set up OpenAI API key
openai.api_key = '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'

# Initialize Flask application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://9b1d-183-82-103-168.ngrok-free.app"}})

def generate_response(prompt):
    # Generate a response from the chat model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Specify the model to use
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]

# Define route for chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_input = data.get('input')
    if user_input:
        bot_response = generate_response(user_input)
        return jsonify({'response': bot_response})
    else:
        return jsonify({'error': 'No input provided'})

# Define route for streaming data chunks
@app.route('/stream_chatbot', methods=['POST'])
def stream_chatbot():
    data = request.get_json()   
    user_input = data.get('input')
    
    if not user_input:
        return jsonify({'error': 'No input provided'})
    
    def generate():
        # Generate a response from the chat model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Specify the model to use
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        
        bot_response = response.choices[0].message["content"]
        yield json.dumps(bot_response) + '\n'
    
    return Response(generate(), content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True)
