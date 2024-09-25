import json
from flask import Flask, request, jsonify
import pandas as pd
import groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the GROQ API key from the environment variables
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in .env file or environment.")

# Initialize the GROQ client
groq_client = groq.Groq(api_key=groq_api_key)

import json  # Add this import to handle JSON


def analyze_sentiment(text):
    prompt = f"Analyze the sentiment of the following text and return only a JSON object with scores for positive, negative, and neutral sentiment: {text}"

    response = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a sentiment analysis expert. Provide sentiment scores as JSON."},
            {"role": "user", "content": prompt}
        ],
        model="mixtral-8x7b-32768",
        temperature=0
    )

    # Print the raw response for debugging
    raw_response = response.choices[0].message.content
    print("Raw API response:", raw_response)

    try:
        # Find the starting point of the JSON object
        json_start = raw_response.index('{')
        json_content = raw_response[json_start:]

        # Remove any text after the closing brace of the JSON object
        closing_brace_index = json_content.index('}') + 1
        json_content = json_content[:closing_brace_index]

        # Parse the JSON content
        sentiment_scores = json.loads(json_content)
    except (ValueError, json.JSONDecodeError) as e:
        raise ValueError(f"Invalid JSON format received from the API: {e}")

    return sentiment_scores


@app.route('/analyze', methods=['POST'])
def analyze_reviews():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        df = pd.read_excel(file)  # Read directly from the uploaded file

        reviews = df['Review'].tolist()[:50]  # Limit to 50 reviews
        results = []
        for Review in reviews:
            sentiment = analyze_sentiment(Review)
            results.append(sentiment)

        return jsonify(results)

    except FileNotFoundError:
        return jsonify({"error": "customer_reviews.xlsx file not found in the project directory"}), 404
    except KeyError:
        return jsonify({"error": "The 'Review' column was not found in the Excel file"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
