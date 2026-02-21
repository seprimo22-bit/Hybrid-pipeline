
from flask import Flask, request, jsonify, render_template
import re
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# =========================================================
# -------------------- RAG ENGINE -------------------------
# =========================================================

class SimpleRAG:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.documents = []

    def build_index(self, documents):
        self.documents = documents
        embeddings = self.model.encode(documents)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))

    def retrieve(self, query, top_k=3):
        if self.index is None:
            return []

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(query_embedding), top_k
        )

        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])

        return results


rag = SimpleRAG()

internal_docs = [
    "Titan A16 is a constraint-first alloy framework.",
    "The coherence ratio measures structural integrity divided by deformation noise.",
    "ORR enforces validation through falsifiable constraint testing.",
    "Geometry-driven metamaterials modulate mechanical properties.",
    "Additive manufacturing introduces microstructural brittleness."
]

rag.build_index(internal_docs)

# =========================================================
# ------------------ HYBRID PIPELINE ----------------------
# =========================================================

TERM_MAP = {
    "metamaterial": ["architected material", "lattice material"],
    "coherence": ["stability", "structural integrity"],
    "geometry optimization": ["design-centered", "architected"]
}

AMBIGUOUS_TERMS = [
    "promising", "may", "potential",
    "suggests", "could", "likely"
]


class HybridPipeline:

    def extract_facts(self, text):
        sentences = re.split(r'[.!?]', text)
        triggers = [
            "developed", "demonstrates", "shows",
            "improves", "reveals", "indicates",
            "introduces", "confirms"
        ]

        return [
            s.strip()
            for s in sentences
            if any(t in s.lower() for t in triggers)
        ]

    def normalize_terms(self, facts):
        normalized = []
        for fact in facts:
            updated = fact
            for canonical, variants in TERM_MAP.items():
                for variant in variants:
                    updated = re.sub(
                        variant, canonical, updated,
                        flags=re.IGNORECASE
                    )
            normalized.append(updated)
        return normalized

    def ambiguity_score(self, text):
        count = sum(text.lower().count(t) for t in AMBIGUOUS_TERMS)
        total = max(len(text.split()), 1)
        return round(count / total, 4)

    def extract_constraints(self, facts):
        return [
            f for f in facts
            if "must" in f.lower() or "requires" in f.lower()
        ]

    def context_alignment_score(self, facts, keywords):
        if not keywords:
            return 0.0

        matches = sum(
            1 for f in facts
            for k in keywords if k.lower() in f.lower()
        )

        return round(matches / max(len(facts), 1), 3)

    def confidence_score(self, facts, ambiguity, alignment):
        base = min(len(facts) * 0.1, 0.5)
        bonus = alignment * 0.3
        penalty = ambiguity * 0.5
        return round(max(base + bonus - penalty, 0), 3)

    def interpret(self, confidence, ambiguity, alignment, retrieved):
        output = []

        if confidence > 0.65:
            output.append("High structural coherence detected.")
        elif confidence > 0.35:
            output.append("Moderate coherence. Further validation advised.")
        else:
            output.append("Low coherence. Analytical instability detected.")

        if ambiguity > 0.02:
            output.append("Ambiguous terminology present.")

        if alignment > 0:
            output.append("Contextual alignment detected.")

        if retrieved:
            output.append("Relevant internal knowledge integrated.")

        return output

    def verification_pass(self, facts):
        return [f for f in facts if len(f.split()) > 4]

    def run(self, article_text, context_keywords=None):
        facts = self.extract_facts(article_text)
        normalized = self.normalize_terms(facts)

        ambiguity = self.ambiguity_score(article_text)
        constraints = self.extract_constraints(normalized)
        alignment = self.context_alignment_score(
            normalized, context_keywords or []
        )

        retrieved = rag.retrieve(" ".join(normalized))
        confidence = self.confidence_score(
            normalized, ambiguity, alignment
        )

        verified = self.verification_pass(normalized)

        classification = {
            "Facts": verified,
            "Hypotheses": [],
            "Analytical Indicators": normalized,
            "Speculation": [],
            "Open Questions": []
        }

        interpretation = self.interpret(
            confidence, ambiguity, alignment, retrieved
        )

        return {
            "classification": classification,
            "constraint_density": len(constraints),
            "context_alignment_score": alignment,
            "ambiguity_score": ambiguity,
            "confidence_score": confidence,
            "retrieved_context": retrieved,
            "interpretation": interpretation
        }


pipeline = HybridPipeline()

# =========================================================
# ---------------------- ROUTES ---------------------------
# =========================================================

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
