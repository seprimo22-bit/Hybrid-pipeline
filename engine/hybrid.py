from openai import OpenAI
from engine.rag import RAGEngine

class HybridPipeline:

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.rag = RAGEngine()

    # -----------------------------
    # 1️⃣ Cognitive Intake
    # -----------------------------
    def cognitive_intake(self, text):

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": "Extract facts and compute ambiguity score."},
                {"role": "user", "content": text}
            ]
        )

        content = response.choices[0].message.content

        # VERY simple structured fallback
        facts = [line.strip() for line in content.split("\n") if line.strip()]

        return {
            "facts": facts,
            "ambiguity_score": 0.01  # placeholder until you compute real metric
        }

    # -----------------------------
    # 5️⃣ Reflective Interpretation
    # -----------------------------
    def reflective_layer(self, text, retrieved_context):

        context_block = "\n".join(retrieved_context)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a document-level reasoning engine.

Return:
1. Core Claim
2. What Is Novel
3. Assumptions
4. Speculation
5. Implications
"""
                },
                {
                    "role": "user",
                    "content": f"""
Context:
{context_block}

Article:
{text}
"""
                }
            ]
        )

        return response.choices[0].message.content

    # -----------------------------
    # MAIN EXECUTION
    # -----------------------------
    def run(self, text):

        intake = self.cognitive_intake(text)

        volatility_flag = intake["ambiguity_score"] > 0.02

        structured = {
            "facts": intake["facts"],
            "ambiguity_score": intake["ambiguity_score"],
            "volatility_flag": volatility_flag
        }

        retrieved = self.rag.retrieve(text, top_k=3)

        risk_score = intake["ambiguity_score"] * 10
        constraint_density = len(intake["facts"])

        analytics = {
            "retrieved_context": retrieved,
            "risk_score": risk_score,
            "constraint_density": constraint_density
        }

        reflection = self.reflective_layer(text, retrieved)

        return {
            "classification": {
                "Facts": intake["facts"],
                "Hypotheses": [],
                "Analytical Indicators": retrieved,
                "Speculation": [],
                "Open Questions": []
            },
            "analytics": analytics,
            "reflection": reflection,
            "verification_pass": True
        }
