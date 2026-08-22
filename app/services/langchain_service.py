import json
import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from ..config import settings


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.1,
    api_key=settings.GROQ_API_KEY,
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI expense analysis assistant.

Analyze the user's expenses and return ONLY one valid JSON object.

Do NOT return:
- <think>
- </think>
- reasoning
- explanations outside JSON
- markdown
- ```json
- ``` 
- any text before or after the JSON

The JSON must contain exactly these fields:

{{
  "total_spending": 0,
  "top_category": "",
  "insight": "",
  "recommendation": ""
}}

Rules:
- total_spending must be a number.
- top_category must be the category with the highest total spending.
- insight should briefly explain the spending pattern.
- recommendation should give one practical suggestion.

Return ONLY the JSON object.
""",
        ),
        (
            "human",
            """
Expenses:

{expenses}
""",
        ),
    ]
)


chain = prompt | llm


def analyze_with_langchain(expenses: str):

    response = chain.invoke(
        {
            "expenses": expenses
        }
    )

    result = response.content

    if not isinstance(result, str):
        result = str(result)

    # Remove <think>...</think> reasoning
    result = re.sub(
        r"<think>.*?</think>",
        "",
        result,
        flags=re.DOTALL | re.IGNORECASE
    )

    # Remove markdown fences
    result = result.replace("```json", "")
    result = result.replace("```", "")

    result = result.strip()

    # Find the first JSON object in the response.
    match = re.search(
        r"\{.*\}",
        result,
        flags=re.DOTALL
    )

    if not match:
        raise ValueError(
            f"AI did not return a JSON object: {result}"
        )

    json_text = match.group(0)

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"AI returned invalid JSON: {result}"
        ) from e

    # Make sure the expected fields exist.
    required_fields = [
        "total_spending",
        "top_category",
        "insight",
        "recommendation",
    ]

    for field in required_fields:
        if field not in parsed:
            raise ValueError(
                f"AI response missing field: {field}"
            )

    return parsed