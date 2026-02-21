from flask import Flask, request, jsonify, render_template
import numpy as np

# Optional semantic search support
try:
    import faiss
    from sentence_transformers import SentenceTransformer
    MODEL_AVAILABLE = True
except:
    MODEL_AVAILABLE = False


app = Flask(__name__)


# ------------------------
# Hybrid Pipeline Engine
# ------------------------

class HybridPipeline:
    def __init__(self):
        self.documents = []
        self.index = None

        if MODEL_AVAILABLE:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
        else:
            self.model = None


    def build_index(self, docs):
        self.documents = docs

        if not MODEL_AVAILABLE:
            return

        embeddings = self.model.encode(docs)
        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings))


    def query(self, text, k=3):
        if not MODEL_AVAILABLE or self.index is None:
            return ["Semantic search unavailable."]

        emb = self.model.encode([text])
        distances, idx = self.index.search(np.array(emb), k)

        return [self.documents[i] for i in idx[0]]


pipeline = HybridPipeline()


# ------------------------
# Routes
# ------------------------

@app.route("/")
def home():
    return "Hybrid Pipeline Running"


@app.route("/index", methods=["POST"])
def index_docs():
    data = request.json.get("documents", [])
    pipeline.build_index(data)
    return jsonify({"status": "indexed", "count": len(data)})


@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "")
    result = pipeline.query(question)
    return jsonify({"response": result})


# ------------------------
# Run Local Only
# ------------------------

if __name__ == "__main__":
    app.run(debug=True)
