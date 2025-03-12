import google.generativeai as genai

genai.configure(api_key="AIzaSyB8iZGW_Kee3nS3uBxIABQnACGg5A97lLU")

try:
    model = genai.GenerativeModel("models/gemini-1.5-pro")  # Use the correct model from list_models()
    response = model.generate_content("Tell me a short story about a cat and a dog.")
    print(response.text)
except Exception as e:
    print("Error:", e)
