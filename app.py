import os
import json
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__, template_folder="templates")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

documents = []


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# DOCUMENT INDEXING (optional)
# -----------------------------
@app.route("/index", methods=["POST"])
def index_docs():
    global documents
    documents = request.json.get("documents", [])
    return jsonify({"indexed": len(documents)})


# -----------------------------
# HYBRID PIPELINE ENGINE
# -----------------------------
@app.route("/ask", methods=["POST"])
def ask():

    question = request.json.get("question", "")
    corpus = "\n\n".join(documents[:5])

    prompt = f"""
You are the Hybrid Integration Pipeline.

Return ONLY valid JSON in this structure:

{{
  "classification": "",
  "reflection": "",
  "analytics": {{}},
  "verified": true
}}

Pipeline method:

1. Separate facts vs assumptions.
2. Stabilize interpretation.
3. Extract analytical constraints.
4. Compare with research corpus:
{corpus}
5. Provide reflective insight.
6. Verify claims carefully.

User input:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(content)
        return jsonify(parsed)
    except:
        return jsonify({
            "classification": "Hybrid Analysis",
            "reflection": content,
            "analytics": {},
            "verified": False
        })


# -----------------------------
# LOCAL RUN / RENDER ENTRY
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
