from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

# --------------------------------------------------
# Flask Setup
# --------------------------------------------------
app = Flask(__name__)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --------------------------------------------------
# HEALTH CHECK ROUTES (IMPORTANT FOR DEBUGGING)
# --------------------------------------------------

@app.route("/test")
def test():
    return "Backend alive."


@app.route("/debug", methods=["POST"])
def debug():
    return jsonify({
        "received": request.get_json()
    })


# --------------------------------------------------
# HYBRID PIPELINE LAYERS
# --------------------------------------------------

def llm_call(system, user):
    """Safe wrapper so failures return readable errors."""
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"LLM ERROR: {str(e)}"


# 1️⃣ Cognitive Intake
def cognitive_intake(text):
    return llm_call(
        "You perform epistemic intake filtering.",
        f"""
Separate factual statements from assumptions.
Do not interpret.

TEXT:
{text}
"""
    )


# 2️⃣ Interpretation Stabilization
def interpretation_stabilization(text):
    return llm_call(
        "You stabilize interpretation.",
        f"""
Normalize ambiguity.
Remove narrative distortion.

TEXT:
{text}
"""
    )


# 3️⃣ Translation Layer
def translation_layer(text):
    return llm_call(
        "Convert reasoning into structured analytic format.",
        f"""
Identify:
- constraints
- entities
- contextual metadata

TEXT:
{text}
"""
    )


# 4️⃣ Analytical Integration
def analytical_integration(text):
    return llm_call(
        "Perform analytical evaluation.",
        f"""
Evaluate:
- constraint density
- decision tension
- analytical indicators

TEXT:
{text}
"""
    )


# 5️⃣ Reflective Interpretation
def reflective_layer(text):
    return llm_call(
        "Provide reflective interpretation.",
        f"""
Translate analysis into human insights.
Highlight uncertainty.
Avoid over-interpretation.

TEXT:
{text}
"""
    )


# 6️⃣ Verification Layer
def verification_layer(text):
    return llm_call(
        "Final epistemic verification.",
        f"""
Verify factual grounding.
Remove analytic drift.

TEXT:
{text}
"""
    )


# 7️⃣ Classification Layer
def classification_layer(text):
    return llm_call(
        "Classify epistemic categories.",
        f"""
Classify into:

Facts
Hypotheses
Indicators
Speculation
Open Questions

TEXT:
{text}
"""
    )


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/run_pipeline", methods=["POST"])
def run_pipeline():

    data = request.get_json()
    user_input = data.get("input", "")

    if not user_input.strip():
        return jsonify({"error": "No input provided."})

    # Pipeline execution
    intake = cognitive_intake(user_input)
    stabilized = interpretation_stabilization(intake)
    structured = translation_layer(stabilized)
    analytics = analytical_integration(structured)
    reflection = reflective_layer(analytics)
    verified = verification_layer(reflection)
    classified = classification_layer(verified)

    return jsonify({
        "result": classified
    })


if __name__ == "__main__":
    app.run(debug=True)
