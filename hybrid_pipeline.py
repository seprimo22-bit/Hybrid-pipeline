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
                continue

    return "\n\n".join(corpus[:5])


# ---------------------------------
# HYBRID PIPELINE CORE
# ---------------------------------

def hybrid_pipeline(payload):

    documents = load_documents()

    # Combine structured input into one reasoning block
    combined_input = "\n".join(
        payload.get("facts", []) +
        payload.get("hypotheses", []) +
        payload.get("speculation", []) +
        payload.get("questions", [])
    )

    prompt = f"""
You are executing the Hybrid Integration Pipeline (HIP).

STRICTLY follow this structure:

1️⃣ Cognitive Intake
- Separate facts vs assumptions.

2️⃣ Interpretation Stabilization
- Remove emotional framing.
- Clarify ambiguity.

3️⃣ Translation Layer
- Extract constraints.
- Identify variables.
- Structure reasoning elements.

4️⃣ Analytical Integration
- Compare with research corpus.
- Identify alignment, contradiction, constraint tension.

5️⃣ Reflective Interpretation
- Translate findings into plain-language insight.

6️⃣ Verification
- Remove unsupported claims.

7️⃣ Final Structured Output (Return EXACT headings):

Facts:
Hypotheses:
Analytical Indicators:
Speculation:
Open Questions:
Reflective Summary:

USER INPUT:
{combined_input}

RESEARCH CORPUS:
{documents}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You are a structured reasoning engine."},
            {"role": "user", "content": prompt}
        ]
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
    try:
        payload = request.json

        if not payload:
            return jsonify({"error": "No input provided"}), 400

        result = hybrid_pipeline(payload)

        return jsonify({
            "status": "success",
            "analysis": result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ---------------------------------
# ENTRY POINT
# ---------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
