import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__, template_folder="templates")


# -----------------------------
# HYBRID PIPELINE CORE (STUB)
# -----------------------------

def run_hybrid_pipeline(data):
    """
    Minimal hybrid logic for now.
    Replace later with ORNS/OpenAI integration.
    """

    facts = data.get("facts", [])
    hypotheses = data.get("hypotheses", [])
    speculation = data.get("speculation", [])
    questions = data.get("questions", [])

    tension_score = len(hypotheses) + len(speculation) + len(questions)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "fact_count": len(facts),
        "hypothesis_count": len(hypotheses),
        "uncertainty_count": tension_score,
        "assessment": "High tension"
        if tension_score > 5
        else "Moderate tension"
        if tension_score > 2
        else "Low tension",
        "input_preview": facts[:1] if facts else []
    }


# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/run", methods=["POST"])
def api_run():
    data = request.json
    result = run_hybrid_pipeline(data)
    return jsonify(result)


# -----------------------------
# RENDER PORT HANDLING
# -----------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
