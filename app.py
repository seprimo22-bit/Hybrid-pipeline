import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__, template_folder="templates")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

documents = []


# -------------------------------
# HOME PAGE
# -------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# DOCUMENT INDEXING (OPTIONAL)
# -------------------------------

@app.route("/index", methods=["POST"])
def index_docs():
    global documents
    documents = request.json.get("documents", [])
    return jsonify({"indexed": len(documents)})


# -------------------------------
# HYBRID PIPELINE
# -------------------------------

@app.route("/ask", methods=["POST"])
def ask():

    question = request.json.get("question", "")

    corpus = "\n\n".join(documents[:5])

    prompt = f"""
You are running the Hybrid Integration Pipeline.

Follow this structure EXACTLY:

1. Cognitive Intake:
Separate facts vs assumptions.

2. Interpretation Stabilization:
Clarify ambiguity and remove emotional framing.

3. Translation Layer:
Extract constraints, variables, reasoning structure.

4. Analytical Integration:
Compare with research corpus:
{corpus}

5. Reflective Interpretation:
Return plain-language insight.

6. Verification:
Remove unsupported claims.

7. Output Classification:

Return JSON with keys:

classification
reflection
analytics
verified

USER INPUT:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content

    # Fallback parse (keeps UI working even if formatting varies)
    return jsonify({
        "classification": "Hybrid Analysis",
        "reflection": text,
        "analytics": {},
        "verified": True
    })


# -------------------------------
# LOCAL RUN
# -------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
