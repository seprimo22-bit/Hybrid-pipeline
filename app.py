from flask import Flask, request, jsonify

app = Flask(__name__)

documents = []

@app.route("/")
def home():
    return "Hybrid Pipeline Live"

@app.route("/index", methods=["POST"])
def index_docs():
    global documents
    documents = request.json.get("documents", [])
    return jsonify({"indexed": len(documents)})

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "")
    
    # Simple keyword matching fallback
    matches = [doc for doc in documents if question.lower() in doc.lower()]
    
    return jsonify({
        "question": question,
        "matches": matches[:3]
    })

if __name__ == "__main__":
    app.run(debug=True)
