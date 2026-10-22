import base64
import json
import os

from groq import Groq


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_receipt(image_bytes: bytes, content_type: str):

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model=os.getenv("GROQ_VISION_MODEL", "qwen/qwen3.8-27b"),
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
Look at this receipt and extract the expense information.

Return ONLY valid JSON in this exact format:

{
  "amount": 0,
  "category": "",
  "description": ""
}

Rules:
- amount must be a number
- category should be something like Food, Shopping, Transport, Bills
- description should briefly describe the purchase
""",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{content_type};base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(
        response.choices[0].message.content
    )
