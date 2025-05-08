from flask import Flask, request, jsonify
from openai import OpenAI  # Correct modern SDK import
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load env variables from .env
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Correct env variable key name (should match .env file)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)  # Instantiate once


@app.route("/generate-list", methods=["POST"])
def generate_list():
    data = request.get_json()
    category = data.get("category", "animals")
    count = data.get("count", 10)

    prompt = f"Give me a list of {count} unique real-world items from category: {category}. The items should be random in theme but all should exist in the real world. Return them in a random order with no explanations or formatting."
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates game items.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=1.0,  
            top_p=0.95,       
            presence_penalty=1.0, 
            frequency_penalty=0.5, 
        )

        raw_output = response.choices[0].message.content

        items = [
            line.strip("1234567890). ").strip()
            for line in raw_output.splitlines()
            if line.strip()
        ]
        return jsonify({"items": items})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
