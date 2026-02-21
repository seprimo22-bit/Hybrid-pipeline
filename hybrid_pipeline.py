from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple in-memory store
documents = []


@app.route("/")
def home():
    return "Hybrid Pipeline is running."


@app.route("/index", methods=["POST"])
def index_docs():
    global documents
    data = request.json.get("documents", [])
    documents = data
    return jsonify({"status": "indexed", "count": len(documents)})


@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "")

    # Simple fallback matching
    matches = [
        doc for doc in documents
        if question.lower() in doc.lower()
    ]

    return jsonify({
        "question": question,
        "matches": matches[:3]
    })


if __name__ == "__main__":
    app.run(debug=True)
