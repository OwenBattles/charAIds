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

    prompt = f"Make a heads-up game with {count} unique singular nouns from category: {category}. Use the least amount of description possible. The items should be in a random order. Return them with every entry on a new line."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106", 
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates game items.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,  
            top_p=1.0,       
        )

        raw_output = response.choices[0].message.content.strip()

        # Primary strategy: split by newline
        items = raw_output.splitlines()

        # Fallback only if clearly comma-separated AND single line
        if len(items) == 1 and ',' in items[0]:
            items = [item.strip() for item in items[0].split(',')]

        # Final cleanup
        items = [item.strip("1234567890). ").strip() for item in items if item.strip()]

        return jsonify({"items": items})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
