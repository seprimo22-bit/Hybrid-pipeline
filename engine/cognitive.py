import re


class CognitivePipeline:

    def extract_facts(self, text):
        sentences = re.split(r'[.!?]', text)

        triggers = [
            "is", "are", "was", "were",
            "shows", "indicates",
            "demonstrates", "confirms"
        ]

        return [
            s.strip()
            for s in sentences
            if any(t in s.lower() for t in triggers)
        ]

    def ambiguity_score(self, text):
        ambiguous = ["may", "might", "could", "possibly", "suggests"]
        hits = sum(text.lower().count(a) for a in ambiguous)

        words = max(len(text.split()), 1)
        return round(hits / words, 3)

    def run(self, article, context=None):
        facts = self.extract_facts(article)
        ambiguity = self.ambiguity_score(article)

        return {
            "facts": facts,
            "ambiguity_score": ambiguity
        }
