from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# -------------------------
# SIMPLE HYBRID ANALYSIS
# -------------------------

def hybrid_analysis(article, context):

    words = article.split()
    word_count = len(words)

    ambiguity_terms = ["may", "might", "could", "possibly", "suggests"]
    ambiguity_hits = sum(article.lower().count(t) for t in ambiguity_terms)

    context_matches = 0
    for word in context:
        if word.lower() in article.lower():
            context_matches += 1

    confidence = round(min((word_count / 100) + (context_matches * 0.1), 1.0), 3)

    return {
        "classification": {
            "Facts": [article[:200]] if article else [],
            "Hypotheses": [],
            "Analytical Indicators": context,
            "Speculation": [],
            "Open Questions": []
        },
        "metrics": {
            "word_count": word_count,
            "ambiguity_hits": ambiguity_hits,
            "context_matches": context_matches,
            "confidence_score": confidence
        }
    }


# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hybrid Test</title>
    </head>
    <body>
        <h1>Hybrid Pipeline Test</h1>

        <textarea id="question" placeholder="Context words"></textarea><br><br>
        <textarea id="article" placeholder="Paste article text"></textarea><br><br>

        <button onclick="run()">Run</button>

        <pre id="output"></pre>

        <script>
        async function run() {
            const article = document.getElementById("article").value;
            const question = document.getElementById("question").value;

            const res = await fetch("/analyze", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    article: article,
                    context: question.split(" ")
                })
            });

            const data = await res.json();
            document.getElementById("output").innerText =
                JSON.stringify(data, null, 2);
        }
        </script>
    </body>
    </html>
    """)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    article = data.get("article", "")
    context = data.get("context", [])

    result = hybrid_analysis(article, context)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
