from flask import Flask, request, jsonify
from openai import OpenAI

client = OpenAI(api_key='')
app = Flask(__name__)

def ask_model(prompt):
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": prompt}
    ])
    return completion.choices[0].message.content.strip()

@app.route('/generate_response', methods=['POST'])
def generate_response():
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    response = ask_model(prompt)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
