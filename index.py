from flask import Flask, request, jsonify
import fasttext
import os
from flask_cors import CORS
import re
from urllib.parse import urlparse
import gdown

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
output = "fasttext_url_classifier_109k_version4_Dataset.ftz"

model = fasttext.load_model(output)

if model:
    return jsonify({"Model loaded successfully in the first block"}), 200
elif not model:
    eturn jsonify({"Model not loaded successfully in the first block of elif"}), 500
    
# try:
#     model = fasttext.load_model(output)
#     return jsonify({"Model loaded successfully"}), 200
    
# except Exception as e:
#     # print(f"Error loading model: {e}")
#     return jasonify({"Model failed to load. This is the exception part"}), 500
#     model = None

# # Helper function to preprocess URLs
# def preprocess_url(url):
#     # Basic preprocessing - you may need to adjust based on your model training
#     parsed = urlparse(url)
#     domain = parsed.netloc
#     path = parsed.path
#     # Convert to lowercase and remove special characters
#     processed = re.sub(r'[^\w\s]', ' ', (domain + path).lower())
#     return processed

def is_valid_url(url):
    """Validate URL format"""
    if not url or not isinstance(url, str):
        return False
    
    # Check if URL is empty or only whitespace
    if not url.strip():
        return False
    
    try:
        result = urlparse(url)
        # Check if URL has at least a scheme and netloc
        return all([result.scheme, result.netloc])
    except:
        return False

@app.route('/api/classify', methods=['POST'])
def classify_url():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500
    
    data = request.json
    if not data or 'url' not in data:
        return jsonify({"error": "URL is required"}), 400
    
    url = data['url']
    
    # Validate URL format
    if not is_valid_url(url):
        return jsonify({"error": "Invalid URL format"}), 400
    
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
