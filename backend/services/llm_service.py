from groq import Groq
from config import Config

client = Groq(api_key=Config.GROQ_API_KEY)


def ask_llm(context, question):

    prompt = f"""
You are an AI Customer Support Assistant.

Use ONLY the context below.

Context:
{context}

Question:
{question}

Return JSON only.

{{
"category":"",
"priority":"",
"confidence":95,
"answer":""
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content