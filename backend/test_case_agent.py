from rag import rag_query
from openrouter_client import call_llm


def generate_test_cases(query):
    """
    Generates well-structured test cases grounded strictly in the retrieved context.
    """

    context = rag_query(query)

    prompt = f"""
You are a Senior QA Engineer.

Using ONLY the context below, generate high-quality test cases.

Context:
{context}

User request: {query}

Rules:
- No hallucinations
- Only use info from context
- Return JSON array

Example format:
[
  {{
    "Test_ID": "TC-001",
    "Feature": "",
    "Scenario": "",
    "Steps": [],
    "Expected": "",
    "Grounded_In": ""
  }}
]
"""

    return call_llm(prompt)
