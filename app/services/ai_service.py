import os
import json

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_expenses(expenses):

    if not expenses:
        return {
            "total_spending": 0,
            "top_category": "None",
            "insight": "You don't have any expenses yet.",
            "recommendation": "Start adding your expenses to get AI insights."
        }

    total_spending = sum(
        expense.amount for expense in expenses
    )

    expense_text = "\n".join(
        [
            f"{expense.category}: €{expense.amount} - {expense.description}"
            for expense in expenses
        ]
    )

    prompt = f"""
You are a financial assistant.

Analyze these expenses:

{expense_text}

Total spending: €{total_spending:.2f}

Return ONLY valid JSON in exactly this format:

{{
  "total_spending": {total_spending:.2f},
  "top_category": "category name",
  "insight": "one short spending insight",
  "recommendation": "one practical recommendation"
}}

Do not add markdown.
Do not add explanations outside the JSON.
Keep the insight and recommendation short.
"""

    response = client.chat.completions.create(
    model=os.getenv("GROQ_TEXT_MODEL", "llama-3.3-70b-versatile"),
    messages=[
        {
            "role": "system",
            "content": "Return ONLY valid JSON. No explanations."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    response_format={"type": "json_object"},
    max_completion_tokens=500,
    temperature=0.7
    )
    
    content = response.choices[0].message.content

    return json.loads(content)
