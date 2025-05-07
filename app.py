from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.getenv("charAIds Key")

app = Flask(__name__)


@app.route("/generate-charades", methods=["POST"])
def generate_charades():
    data = request.get_json()
    category = data.get("category", "")

    if not category:
        return jsonify({"error": "Category is required"}), 400

    prompt = (
        f"Give me a list of 30 charades "
        f"for the category '{category}'. Format it as a plain list with no numbering."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=100,
        )

        charades_raw = response["choices"][0]["message"]["content"]
        charades_list = [
            line.strip("-• ").strip()
            for line in charades_raw.split("\n")
            if line.strip()
        ]

        return jsonify({"charades": charades_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
