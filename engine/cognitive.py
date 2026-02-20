import re

AMBIGUOUS_TERMS = [
    "may", "might", "could", "possibly", "suggests", "likely"
]

class CognitivePipeline:

    def extract_facts(self, text):
        sentences = re.split(r'[.!?]', text)
        triggers = [
            "is", "are", "was", "were",
            "shows", "indicates",
            "demonstrates", "confirms",
            "developed", "reveals"
        ]

        return [
            s.strip()
            for s in sentences
            if any(t in s.lower() for t in triggers)
        ]

    def ambiguity_score(self, text):
        hits = sum(text.lower().count(a) for a in AMBIGUOUS_TERMS)
        words = max(len(text.split()), 1)
        return round(hits / words, 4)

    def run(self, text, context=None):
        facts = self.extract_facts(text)
        ambiguity = self.ambiguity_score(text)

        return {
            "facts": facts,
            "ambiguity_score": ambiguity,
            "context_terms": context or []
        }
