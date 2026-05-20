from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

chat_history = [
    {
        "role": "system",
        "content": "Du bist Garmin AI. Du bist lustig, hilfst bei Technik und redest auf Deutsch."
    }
]

@app.route("/frage", methods=["POST"])
def frage():

    data = request.json
    text = data["text"]

    chat_history.append({
        "role": "user",
        "content": text
    })

    response = ollama.chat(
        model="llama3",
        messages=chat_history
    )

    antwort = response["message"]["content"]

    chat_history.append({
        "role": "assistant",
        "content": antwort
    })

    return jsonify({
        "antwort": antwort
    })

if __name__ == "__main__":
    app.run(port=5000)
