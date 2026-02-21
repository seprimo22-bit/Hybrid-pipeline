from flask import Flask, render_template, request, jsonify
from engine.hybrid import HybridPipeline

app = Flask(__name__)
pipeline = HybridPipeline()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()
    question = data.get("question", "")

    result = pipeline.run(question)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
