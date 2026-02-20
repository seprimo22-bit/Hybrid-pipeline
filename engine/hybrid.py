def reflective_layer(self, text, retrieved_context):

    context_block = "\n".join(retrieved_context)

    response = self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are a document-level reasoning engine.

Analyze the ARTICLE, not its sentences.

Return structured output with:

1. Core Claim (What is the main discovery?)
2. What Is Actually Novel?
3. Underlying Assumptions
4. What Is Unproven or Speculative?
5. Practical Implications
6. What Should Be Investigated Next?
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
