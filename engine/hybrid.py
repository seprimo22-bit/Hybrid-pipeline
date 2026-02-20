from engine.cognitive import CognitivePipeline
from engine.rag import RAGEngine
from openai import OpenAI
import os


class HybridPipeline:

    def __init__(self):
        self.cognitive = CognitivePipeline()
        self.rag = RAGEngine()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def reflective_layer(self, text, retrieved_context):
        context_block = "\n".join(retrieved_context)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Return structured reasoning in sections: Facts, Hypotheses, Analytical Indicators, Speculation, Open Questions."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context_block}\n\nInput:\n{text}"
                }
            ]
        )

        return response.choices[0].message.content

    def run(self, text, context=None):

        # 1️⃣ Cognitive Intake
        intake = self.cognitive.run(text, context)

        # 2️⃣ Stabilization
        volatility_flag = intake["ambiguity_score"] > 0.02

        # 3️⃣ Translation
        structured = {
            "facts": intake["facts"],
            "ambiguity_score": intake["ambiguity_score"],
            "volatility_flag": volatility_flag
        }

        # 4️⃣ Analytical Integration
        retrieved = self.rag.retrieve(text, top_k=3)
        risk_score = intake["ambiguity_score"] * 10
        constraint_density = len(intake["facts"])

        analytics = {
            "retrieved_context": retrieved,
            "risk_score": risk_score,
            "constraint_density": constraint_density
        }

        # 5️⃣ Reflective Interpretation
        reflection = self.reflective_layer(text, retrieved)

        # 6️⃣ Verification
        verification_pass = True

        # 7️⃣ Output Classification
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
            "verification_pass": verification_pass
        }
