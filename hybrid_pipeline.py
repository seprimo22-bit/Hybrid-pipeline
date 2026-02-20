from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# -------------------------
# Home Route
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# Run Hybrid Pipeline Route
# -------------------------
@app.route("/run_pipeline", methods=["POST"])
def run_pipeline():
    data = request.get_json()

    user_input = data.get("input", "")

    # Simulated Hybrid Pipeline Processing
    result = {
        "status": "success",
        "classification": {
            "Facts": [],
            "Hypotheses": [],
            "Analytical Indicators": [],
            "Speculation": [],
            "Open Questions": []
        },
        "received_input": user_input,
        "message": "Hybrid Pipeline executed successfully."
    }

    return jsonify(result)


# -------------------------
# Run Server (local only)
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
