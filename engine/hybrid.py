
from openai import OpenAI
from engine.cognitive import CognitivePipeline
from engine.rag import RAGEngine
import os


class HybridPipeline:

    def __init__(self, api_key=None):

        # API key handling (safe for Render)
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")

        self.client = OpenAI(api_key=api_key)

        # Subsystems
        self.cognitive = CognitivePipeline(self.client)
        self.rag = RAGEngine()

    # -------------------------------------------------
    # 1️⃣ Cognitive Intake
    # -------------------------------------------------
    def cognitive_intake(self, text):
        return self.cognitive.process(text)

    # -------------------------------------------------
    # 5️⃣ Reflective Interpretation
    # -------------------------------------------------
    def reflective_layer(self, text, retrieved_context):

        context_block = "\n".join(retrieved_context)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": """
You are a document-level reasoning engine.

Return structured output with:

1. Core Claim
2. What Is Novel
3. Assumptions
4. What Is Speculative
5. Practical Implications
6. What Should Be Investigated Next
"""
                },
                {
                    "role": "user",
                    "content": f"""
Context:
{context_block}

ARTICLE:
{text}
"""
                }
            ]
        )

        return response.choices[0].message.content

    # -------------------------------------------------
    # MAIN EXECUTION
    # -------------------------------------------------
    def run(self, text):

        # 1️⃣ Cognitive Intake
        intake = self.cognitive_intake(text)

        facts = intake.get("facts", [])
        ambiguity_score = intake.get("ambiguity_score", 0.0)

        # 2️⃣ Stabilization
        volatility_flag = ambiguity_score > 0.02

        # 3️⃣ Translation
        structured = {
            "facts": facts,
            "ambiguity_score": ambiguity_score,
            "volatility_flag": volatility_flag
        }

        # 4️⃣ Analytical Integration
        retrieved = self.rag.retrieve(text, top_k=3)

        risk_score = ambiguity_score * 10
        constraint_density = len(facts)

        analytics = {
            "retrieved_context": retrieved,
            "risk_score": risk_score,
            "constraint_density": constraint_density
        }

        # 5️⃣ Reflective Interpretation
        reflection = self.reflective_layer(text, retrieved)

        # 6️⃣ Verification
        verification_pass = True

        # 7️⃣ Classification
        return {
            "classification": {
                "Facts": facts,
                "Hypotheses": [],
                "Analytical Indicators": retrieved,
                "Speculation": [],
                "Open Questions": []
            },
            "analytics": analytics,
            "reflection": reflection,
            "verification_pass": verification_pass
        }
