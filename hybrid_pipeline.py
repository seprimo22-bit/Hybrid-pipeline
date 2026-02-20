from flask import Flask, request, jsonify, render_template

from engine.hybrid import HybridPipeline

app = Flask(__name__)

# Initialize hybrid engine
pipeline = HybridPipeline()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    article = data.get("article", "")
    context = data.get("context", [])

    result = pipeline.run(article, context)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
