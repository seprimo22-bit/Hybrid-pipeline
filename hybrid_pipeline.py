from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------------------------
# 1️⃣ Cognitive Intake Layer
# ---------------------------
def cognitive_intake(text):
    prompt = f"""
Separate factual statements from assumptions in the text below.
Do not interpret. Do not summarize.
Return:
- factual_statements
- assumptions

Text:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "You perform epistemic intake filtering."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# ---------------------------
# 2️⃣ Interpretation Stabilization
# ---------------------------
def interpretation_stabilization(text):
    prompt = f"""
Normalize ambiguity and remove emotional or narrative distortion.
Return only stabilized interpretation.

Text:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "You stabilize interpretation and reduce volatility."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# ---------------------------
# 3️⃣ Translation & Structuring
# ---------------------------
def translation_layer(text):
    prompt = f"""
Convert the text into structured analytical data.
Identify:
- constraints
- entities
- contextual metadata

Text:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "You convert reasoning into structured analytic format."},
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
- constraint density
- decision tension
- analytical indicators

Text:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "You perform analytical evaluation."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# ---------------------------
# 5️⃣ Reflective Interpretation
# ---------------------------
def reflective_layer(text):
    prompt = f"""
Translate the analytical results into human-readable insights.
Highlight uncertainty.
Prevent over-interpretation.

Text:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "You provide reflective interpretation."},
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
Confirm epistemic integrity.

Text:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "You perform final verification pass."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# ---------------------------
# 7️⃣ Output Classification
# ---------------------------
def classification_layer(text):
    prompt = f"""
Classify the content into:
- Facts
- Hypotheses
- Analytical Indicators
- Speculation
- Open Questions

Text:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "You classify epistemic categories precisely."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# ---------------------------
# Flask Routes
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/run_pipeline", methods=["POST"])
def run_pipeline():

    data = request.get_json()
    user_input = data.get("input", "")

    if not user_input.strip():
        return jsonify({"error": "No input provided."})

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
