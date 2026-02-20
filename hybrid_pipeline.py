import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify


# -----------------------------
# APP SETUP
# -----------------------------

app = Flask(__name__, template_folder="templates")

DOCUMENT_DIR = "Documents"


# -----------------------------
# DOCUMENT LOADER
# -----------------------------

def load_documents():
    docs = []

    if not os.path.exists(DOCUMENT_DIR):
        return docs

    for file in os.listdir(DOCUMENT_DIR):
        path = os.path.join(DOCUMENT_DIR, file)

        try:
            if file.endswith(".txt"):
                with open(path, "r", encoding="utf-8") as f:
                    docs.append({
                        "name": file,
                        "content": f.read()
                    })

            elif file.endswith(".json"):
                with open(path, "r", encoding="utf-8") as f:
                    docs.append({
                        "name": file,
                        "content": json.load(f)
                    })

        except Exception as e:
            print(f"Document load error: {file}", e)

    return docs


# -----------------------------
# HYBRID PIPELINE CORE
# -----------------------------

def create_payload(input_data, documents):
    return {
        "facts": input_data.get("facts", []),
        "hypotheses": input_data.get("hypotheses", []),
        "uncertainties": (
            input_data.get("speculation", [])
            + input_data.get("questions", [])
        ),
        "documents": documents,
        "metadata": {
            "timestamp": datetime.utcnow().isoformat(),
            "source": input_data.get("source", "manual-input")
        }
    }


def translate_for_orns(payload):
    return {
        "fact_count": len(payload["facts"]),
        "hypothesis_count": len(payload["hypotheses"]),
        "uncertainty_count": len(payload["uncertainties"]),
        "document_count": len(payload["documents"]),
        "metadata": payload["metadata"]
    }


def run_orns_analysis(data):
    # Replace with real ORNS engine later
    score = data["hypothesis_count"] + data["uncertainty_count"]

    return {
        "risk_level": "High" if score > 5 else "Moderate",
        "score": score,
        "analysis_time": datetime.utcnow().isoformat()
    }


def interpret_results(payload, analysis):

    summary = (
        "Elevated analytical tension detected."
        if analysis["risk_level"] == "High"
        else "Moderate analytical tension."
    )

    return {
        "summary": summary,
        "analysis": analysis,
        "documents_loaded": len(payload["documents"]),
        "facts": payload["facts"],
        "hypotheses": payload["hypotheses"],
        "uncertainties": payload["uncertainties"]
    }


def run_hybrid_pipeline(input_data):

    documents = load_documents()

    payload = create_payload(input_data, documents)

    structured = translate_for_orns(payload)

    analysis = run_orns_analysis(structured)

    return interpret_results(payload, analysis)


# -----------------------------
# WEB ROUTES
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":
        try:
            input_data = request.get_json()
            result = run_hybrid_pipeline(input_data)
        except Exception as e:
            result = {"error": str(e)}

    return render_template("index.html", result=result)


@app.route("/api/run", methods=["POST"])
def api_run():

    input_data = request.json
    result = run_hybrid_pipeline(input_data)

    return jsonify(result)


# -----------------------------
# RUN SERVER
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
