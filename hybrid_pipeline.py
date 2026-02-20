from flask import Flask, request, jsonify, render_template
import re
import faiss
import numpy as np
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
        if self.index is None or not self.documents:
            return []

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding), top_k)

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

    # 1️⃣ Cognitive Intake Layer
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

    # 2️⃣ Interpretation Stabilization Layer
    def normalize_terms(self, facts):
        normalized = []
        for fact in facts:
            updated = fact
            for canonical, variants in TERM_MAP.items():
                for variant in variants:
                    updated = re.sub(
                        variant,
                        canonical,
                        updated,
                        flags=re.IGNORECASE
                    )
            normalized.append(updated)
        return normalized

    def ambiguity_score(self, text):
        count = sum(text.lower().count(term) for term in AMBIGUOUS_TERMS)
        total_words = max(len(text.split()), 1)
        return round(count / total_words, 4)

    # 3️⃣ Translation & Structuring Layer
    def extract_constraints(self, facts):
        constraints = []
        for fact in facts:
            if "must" in fact.lower() or "requires" in fact.lower():
                constraints.append(fact)
        return constraints

    def context_alignment_score(self, facts, context_keywords):
        if not context_keywords:
            return 0.0

        matches = 0
        for fact in facts:
            for keyword in context_keywords:
                if keyword.lower() in fact.lower():
                    matches += 1

        return round(matches / max(len(facts), 1), 3)

    # 4️⃣ Analytical Integration Layer
    def confidence_score(self, facts, ambiguity, alignment):
        base = min(len(facts) * 0.1, 0.5)
        bonus = alignment * 0.3
        penalty = ambiguity * 0.5
        return round(max(base + bonus - penalty, 0), 3)

    # 5️⃣ Reflective Interpretation Layer
    def interpret(self, confidence, ambiguity, alignment, retrieved):
        interpretation = []

        if confidence > 0.65:
            interpretation.append("High structural coherence detected.")
        elif confidence > 0.35:
            interpretation.append("Moderate coherence. Further validation advised.")
        else:
            interpretation.append("Low coherence. Analytical instability detected.")

        if ambiguity > 0.02:
            interpretation.append("Ambiguous terminology present.")

        if alignment > 0:
            interpretation.append("Contextual alignment detected.")

        if retrieved:
            interpretation.append("Relevant internal knowledge integrated.")

        return interpretation

    # 6️⃣ Verification Loop
    def verification_pass(self, facts):
        return [f for f in facts if len(f.split()) > 4]

    # FULL HYBRID EXECUTION
    def run(self, article_text, context_keywords=None):

        # Cognitive intake
        facts = self.extract_facts(article_text)

        # Stabilization
        normalized = self.normalize_terms(facts)
        ambiguity = self.ambiguity_score(article_text)

        # Translation
        constraints = self.extract_constraints(normalized)
        alignment = self.context_alignment_score(normalized, context_keywords or [])

        # Analytical
        retrieved = rag.retrieve(" ".join(normalized), top_k=3)
        confidence = self.confidence_score(normalized, ambiguity, alignment)

        # Verification
        verified = self.verification_pass(normalized)

        # Classification
        classification = {
            "Facts": verified,
            "Hypotheses": [],
            "Analytical Indicators": normalized,
            "Speculation": [],
            "Open Questions": []
        }

        # Interpretation
        interpretation = self.interpret(confidence, ambiguity, alignment, retrieved)

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
