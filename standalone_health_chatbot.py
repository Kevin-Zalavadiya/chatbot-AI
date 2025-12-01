import google.generativeai as genai
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import re

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Gemini Chatbot Class
class HealthChatbot:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def extract_symptoms(self, text):
        prompt = f"""
        Extract symptoms from this message: "{text}"
        Return only a Python list of symptoms in lowercase.
        Example: ["fever", "headache"]
        
        Rules:
        - Extract ALL symptoms mentioned
        - Convert variations: "head hurting" → "headache", "feverish" → "fever", "body pain" → "body ache"
        - If only 1 symptom found, still return it
        - If no clear symptoms, return ["fever", "headache"] (default symptoms)
        - Always return a list, never return empty
        """
        response = self.model.generate_content(prompt)
        try:
            symptoms = eval(response.text.strip())
            if not symptoms or symptoms == []:
                return ["fever", "headache"]
            return symptoms
        except:
            return ["fever", "headache"]
    
    def detect_treatment_type(self, message):
        message = message.lower()
        if "ayurved" in message:
            return "ayurveda"
        elif "homeopath" in message:
            return "homeopathy" 
        elif "home remedy" in message or "home remedies" in message:
            return "home remedy"
        else:
            return "all"
    
    def get_treatment(self, symptoms, treatment_type):
        symptoms_str = ", ".join(symptoms)
        
        if treatment_type == "ayurveda":
            prompt = f"""
            Provide ONLY Ayurvedic treatment for: {symptoms_str}
            
            Format your response cleanly with HTML:
            <p><strong>Ayurvedic Medicine:</strong> [medicine name]</p>
            <p><strong>Dosage:</strong> [how to take]</p>
            <p><strong>Precautions:</strong> [what to avoid]</p>
            <p><strong>Home Tips:</strong> [additional advice]</p>
            
            Keep response focused only on Ayurvedic treatments.
            Include medical disclaimer at the end.
            Use simple formatting without excessive asterisks or markdown.
            """
        
        elif treatment_type == "homeopathy":
            prompt = f"""
            Provide ONLY Homeopathic treatment for: {symptoms_str}
            
            Format your response cleanly with HTML:
            <p><strong>Homeopathic Medicine:</strong> [medicine name]</p>
            <p><strong>Dosage:</strong> [how to take]</p>
            <p><strong>Precautions:</strong> [what to avoid]</p>
            <p><strong>Home Tips:</strong> [additional advice]</p>
            
            Keep response focused only on Homeopathic treatments.
            Include medical disclaimer at the end.
            Use simple formatting without excessive asterisks or markdown.
            """
        
        elif treatment_type == "home remedy":
            prompt = f"""
            Provide ONLY Home Remedies for: {symptoms_str}
            
            Format your response cleanly with HTML:
            <p><strong>Home Remedy:</strong> [remedy name]</p>
            <p><strong>How to Use:</strong> [instructions]</p>
            <p><strong>Precautions:</strong> [warnings]</p>
            <p><strong>Benefits:</strong> [why it helps]</p>
            
            Keep response focused only on natural home remedies.
            Include medical disclaimer at the end.
            Use simple formatting without excessive asterisks or markdown.
            """
        
        else:  # all types
            prompt = f"""
            Provide treatments for: {symptoms_str}
            Include all three types: Ayurvedic, Homeopathy, and Home Remedies.
            
            Format your response cleanly with HTML:
            <p><strong>Ayurvedic:</strong> [medicine] - [dosage]</p>
            <p><strong>Homeopathy:</strong> [medicine] - [dosage]</p>
            <p><strong>Home Remedy:</strong> [remedy] - [how to use]</p>
            
            Keep each treatment type separate and clear.
            Include medical disclaimer at the end.
            Use simple formatting without excessive asterisks or markdown.
            """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def chat(self, user_message):
        symptoms = self.extract_symptoms(user_message)
        treatment_type = self.detect_treatment_type(user_message)
        
        return self.get_treatment(symptoms, treatment_type)

# Initialize chatbot
API_KEY = "AIzaSyCLcDWRmx4F-aHMuXqj0Ot8VGkYEateK8w"  # Update this with your API key
bot = HealthChatbot(API_KEY)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌿 Ayurvedic Health Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .chat-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 800px;
            height: 80vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chat-header {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }

        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f9f9f9;
        }

        .message {
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 18px;
            max-width: 80%;
            word-wrap: break-word;
        }

        .user-message {
            background: #007bff;
            color: white;
            margin-left: auto;
            text-align: right;
        }

        .bot-message {
            background: #e9ecef;
            color: #333;
            margin-right: auto;
        }

        .chat-input {
            padding: 20px;
            background: white;
            border-top: 1px solid #ddd;
            display: flex;
            gap: 10px;
        }

        .message-input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }

        .message-input:focus {
            border-color: #4CAF50;
        }

        .send-button {
            padding: 12px 24px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: background 0.3s;
        }

        .send-button:hover {
            background: #45a049;
        }

        .send-button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }

        .typing-indicator {
            display: none;
            color: #666;
            font-style: italic;
            padding: 12px 16px;
            background: #e9ecef;
            border-radius: 18px;
            margin-right: auto;
            max-width: 80%;
        }

        .examples {
            padding: 10px 20px;
            background: #f0f8ff;
            border-top: 1px solid #ddd;
        }

        .examples h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 14px;
        }

        .example-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .example-btn {
            padding: 6px 12px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            font-size: 12px;
            transition: background 0.3s;
        }

        .example-btn:hover {
            background: #0056b3;
        }

        .message-text strong {
            color: #2c3e50;
            font-weight: 600;
        }

        .message-text p {
            margin: 8px 0;
        }

        @media (max-width: 600px) {
            .chat-container {
                width: 95%;
                height: 90vh;
            }
            
            .message {
                max-width: 90%;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            🌿 Ayurvedic Health Chatbot
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="message bot-message">
                🤖 Hello! I'm your Ayurvedic health assistant. I can help you with:
                <br><br>
                🌿 <strong>Ayurvedic treatments</strong><br>
                🌸 <strong>Homeopathic remedies</strong><br>
                🏠 <strong>Home remedies</strong><br><br>
                Just describe your symptoms naturally, like "I have fever and headache" or specify a treatment type like "ayurvedic treatment for cold".
            </div>
        </div>
        
        <div class="examples">
            <h3>💡 Try these examples:</h3>
            <div class="example-buttons">
                <button class="example-btn" onclick="sendExample('I have fever and headache')">Fever & Headache</button>
                <button class="example-btn" onclick="sendExample('ayurvedic treatment for cold')">Ayurvedic for Cold</button>
                <button class="example-btn" onclick="sendExample('home remedies for stomach pain')">Home Remedies</button>
                <button class="example-btn" onclick="sendExample('homeopathy for anxiety')">Homeopathy</button>
            </div>
        </div>
        
        <div class="chat-input">
            <input type="text" id="messageInput" class="message-input" 
                   placeholder="Describe your symptoms..." 
                   onkeypress="handleKeyPress(event)">
            <button id="sendButton" class="send-button" onclick="sendMessage()">Send</button>
        </div>
        
        <div class="typing-indicator" id="typingIndicator">
            🤖 Thinking...
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        const typingIndicator = document.getElementById('typingIndicator');

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function sendExample(message) {
            messageInput.value = message;
            sendMessage();
        }

        function addMessage(message, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            messageDiv.innerHTML = message;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function showTyping() {
            typingIndicator.style.display = 'block';
            chatMessages.appendChild(typingIndicator);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function hideTyping() {
            typingIndicator.style.display = 'none';
        }

        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            addMessage(message, true);
            messageInput.value = '';
            
            sendButton.disabled = true;
            showTyping();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                
                hideTyping();
                
                if (data.success) {
                    addMessage(data.response);
                } else {
                    addMessage('❌ Sorry, I encountered an error. Please try again.');
                }
            } catch (error) {
                hideTyping();
                addMessage('❌ Connection error. Please check if the server is running.');
            }
            
            sendButton.disabled = false;
            messageInput.focus();
        }

        window.onload = () => {
            messageInput.focus();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        user_message = data.get('message', '')
        if not user_message.strip():
            return jsonify({
                'success': False,
                'error': 'Please enter a message'
            }), 400
        
        response = bot.chat(user_message)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🌿 Starting Standalone Health Chatbot...")
    print("📍 Open your browser to: http://localhost:5000")
    print("🔑 Make sure you have a valid Gemini API key!")
    print("=" * 50)
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
