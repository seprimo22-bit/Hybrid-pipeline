from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

# -----------------------------
# Flask Initialization (FIXED)
# -----------------------------
app = Flask(__name__)

# -----------------------------
# OpenAI Client
# -----------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ==========================================================
# 🟡 HYBRID PIPELINE — FULL 7-LAYER STRUCTURE
# ==========================================================

MODEL = "gpt-4o-mini"  # Accessible + stable on Render


# ---------------------------
# 1️⃣ Cognitive Intake Layer
# ---------------------------
def cognitive_intake(text):

    prompt = f"""
Separate factual statements from assumptions.

Return ONLY:

FACTUAL_STATEMENTS:
ASSUMPTIONS:

Text:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": "Epistemic intake filtering."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ---------------------------
# 2️⃣ Interpretation Stabilization
# ---------------------------
def interpretation_stabilization(text):

    prompt = f"""
Normalize ambiguity.
Remove narrative distortion.
Preserve factual meaning.

Text:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": "Interpretation stabilization."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ---------------------------
# 3️⃣ Translation Layer
# ---------------------------
def translation_layer(text):

    prompt = f"""
Convert reasoning into structured analytical data.

Identify:
- Constraints
- Entities
- Contextual metadata

Text:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": "Analytical structuring."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ---------------------------
# 4️⃣ Analytical Integration
# ---------------------------
def analytical_integration(text):

    prompt = f"""
Perform analytical integration.

Evaluate:
- Constraint density
- Decision tension
- Analytical indicators

Text:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": "Analytical integration."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ---------------------------
# 5️⃣ Reflective Interpretation
# ---------------------------
def reflective_layer(text):

    prompt = f"""
Translate analytics into human-readable insight.

Highlight uncertainty.
Avoid over-interpretation.

Text:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": "Reflective interpretation."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ---------------------------
# 6️⃣ Verification Loop
# ---------------------------
def verification_layer(text):

    prompt = f"""
Verify factual grounding.
Remove analytical drift.

Text:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": "Verification pass."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ---------------------------
# 7️⃣ Final Classification
# ---------------------------
def classification_layer(text):

    prompt = f"""
Classify content into:

Facts:
Hypotheses:
Analytical Indicators:
Speculation:
Open Questions:

Text:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": "Final epistemic classification."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ==========================================================
# 🌐 Flask Routes
# ==========================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/run_pipeline", methods=["POST"])
def run_pipeline():

    try:
        data = request.get_json()
        user_input = data.get("input", "")

        if not user_input.strip():
            return jsonify({"error": "No input provided."})

        # Run full HIP pipeline
        intake = cognitive_intake(user_input)
        stabilized = interpretation_stabilization(intake)
        structured = translation_layer(stabilized)
        analytics = analytical_integration(structured)
        reflection = reflective_layer(analytics)
        verified = verification_layer(reflection)
        classified = classification_layer(verified)

        return jsonify({"result": classified})

    except Exception as e:
        # VERY IMPORTANT for Render debugging
        return jsonify({"error": str(e)})


# ==========================================================
# Local Dev Only
# ==========================================================
if __name__ == "__main__":
    app.run(debug=True)
