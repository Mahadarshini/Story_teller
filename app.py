from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API key
GEMINI_API_KEY = "AIzaSyB8iZGW_Kee3nS3uBxIABQnACGg5A97lLU"
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/generate_story', methods=['POST'])
def generate_story():
    data = request.json
    prompt = data.get("prompt", "Tell me a story")

    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro")  # Ensure correct model name
        response = model.generate_content(prompt)
        
        return jsonify({"story": response.text})
    
    except Exception as e:
        print("Error:", str(e))  # Print the full error message in the terminal
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
