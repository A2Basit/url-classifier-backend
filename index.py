from flask import Flask, request, jsonify
import fasttext
import os
from flask_cors import CORS
import re
from urllib.parse import urlparse

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the FastText model
# Note: You'll need to upload your model file to Vercel
model_path = os.path.join(os.path.dirname(__file__), "E:/FYP/extension/url-classifier-web/backend/model.ftz")
model = None

try:
    model = fasttext.load_model(model_path)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")

# # Helper function to preprocess URLs
# def preprocess_url(url):
#     # Basic preprocessing - you may need to adjust based on your model training
#     parsed = urlparse(url)
#     domain = parsed.netloc
#     path = parsed.path
#     # Convert to lowercase and remove special characters
#     processed = re.sub(r'[^\w\s]', ' ', (domain + path).lower())
#     return processed

@app.route('/api/classify', methods=['POST'])
def classify_url():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500
    
    data = request.json
    if not data or 'url' not in data:
        return jsonify({"error": "URL is required"}), 400
    
    url = data['url']
    try:
        # Preprocess the URL
        # processed_url = preprocess_url(url)
        
        # Get prediction from FastText model
        prediction = model.predict(url)
        
        # Extract the category (removing '__label__' prefix if present)
        category = prediction[0][0]
        if category.startswith('__label__'):
            category = category[9:]
        
        confidence = float(prediction[1][0])
        
        return jsonify({
            "category": category,
            "confidence": confidence,
            "url": url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# For local development
if __name__ == '__main__':
    app.run(port=5328, debug=True)