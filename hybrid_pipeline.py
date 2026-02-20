from flask import Flask, request, jsonify, render_template
from engine.hybrid import HybridPipeline

app = Flask(__name__)
pipeline = HybridPipeline()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    article = data.get("article", "")
    question = data.get("question", "")

    combined_input = article + "\n\n" + question

    result = pipeline.run(combined_input, question.split())

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
