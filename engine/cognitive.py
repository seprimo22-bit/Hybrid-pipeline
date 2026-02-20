class CognitivePipeline:

    def __init__(self, client):
        self.client = client

    def process(self, text):

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "Extract factual statements and estimate ambiguity score (0.0 to 1.0)."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        content = response.choices[0].message.content

        facts = [
            line.strip()
            for line in content.split("\n")
            if line.strip()
        ]

        return {
            "facts": facts,
            "ambiguity_score": 0.01  # placeholder until formal scoring logic added
        }
