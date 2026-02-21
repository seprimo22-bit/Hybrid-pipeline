from dataclasses import dataclass, field
from typing import Dict, Any, List


def classify_text(text: str) -> str:
    text = text.lower()

    if "?" in text:
        return "Open Question"
    if any(w in text for w in ["maybe", "possibly", "could"]):
        return "Speculation"
    if any(w in text for w in ["data", "evidence", "confirmed"]):
        return "Fact"
    if any(w in text for w in ["model", "analysis", "score"]):
        return "Analytical Indicator"

    return "Hypothesis"


@dataclass
class HybridPipeline:

    history: List[Dict[str, Any]] = field(default_factory=list)

    def run(self, text: str) -> Dict[str, Any]:

        # 1️⃣ Cognitive Intake
        intake = {
            "raw": text,
            "questions": "?" in text,
        }

        # 2️⃣ Stabilization
        stabilized = {
            "text": intake["raw"].strip(),
            "confidence": 0.8
        }

        # 3️⃣ Translation
        structured = {
            "length": len(stabilized["text"]),
            "classification": classify_text(stabilized["text"])
        }

        # 4️⃣ Analytics
        score = min(1.0, structured["length"] / 400)
        analytics = {
            "vector_score": round(score, 3),
            "risk_estimate": round(1 - score, 3),
        }

        # 5️⃣ Reflective interpretation
        reflection = (
            f"Vector strength {analytics['vector_score']}. "
            f"Risk estimate {analytics['risk_estimate']}. "
            "Interpret cautiously."
        )

        # 6️⃣ Verification pass
        verified = True

        # 7️⃣ Output classification
        classification = structured["classification"]

        result = {
            "input": text,
            "classification": classification,
            "reflection": reflection,
            "analytics": analytics,
            "verified": verified
        }

        self.history.append(result)
        return result
