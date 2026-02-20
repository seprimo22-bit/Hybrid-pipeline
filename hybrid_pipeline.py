import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__, template_folder="templates")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DOCUMENT_DIR = "Documents"


# ---------------------------------
# DOCUMENT LOADER
# ---------------------------------

def load_documents():
    corpus = []

    if not os.path.exists(DOCUMENT_DIR):
        return ""

    for file in os.listdir(DOCUMENT_DIR):
        if file.endswith(".txt"):
            path = os.path.join(DOCUMENT_DIR, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    corpus.append(f.read())
            except Exception:
                pass

    return "\n\n".join(corpus[:5])


# ---------------------------------
# HYBRID PIPELINE CORE
# ---------------------------------

def hybrid_pipeline(user_input):

    documents = load_documents()

    prompt = f"""
You are running a Hybrid Integration Pipeline.

This pipeline bridges human reasoning clarity and analytical computation.

Follow this EXACT flow:

1. Cognitive Intake:
Separate facts vs assumptions from the user input.

2. Interpretation Stabilization:
Remove emotional framing, clarify ambiguity.

3. Translation Layer:
Convert reasoning into structured analytical elements.

4. Analytical Integration:
Compare reasoning with provided research corpus.
Identify alignments, contradictions, constraint tensions.

5. Reflective Interpretation:
Translate analytics into plain human insight.

6. Verification:
Ensure no unsupported claims remain.

7. Output Classification:
Return structured sections:

Facts:
Hypotheses:
Analytical Indicators:
Speculation:
Open Questions:
Reflective Summary:

USER INPUT:
{user_input}

RESEARCH DOCUMENTS:
{documents}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ---------------------------------
# ROUTES
# ---------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/run", methods=["POST"])
def run_pipeline():
    data = request.json
    text = data.get("input", "")

    result = hybrid_pipeline(text)

    return jsonify({"analysis": result})


# ---------------------------------
# LOCAL / RENDER ENTRY
# ---------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
