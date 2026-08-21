# base/service.py

import os
from google import genai


def build_prompt(category_summary):
    if not category_summary:
        return "The user has no recorded expenses yet. Let them know there's nothing to summarize."

    lines = [f"{item['category']}: ₹{item['total']}" for item in category_summary]
    data_str = ", ".join(lines)

    return (
        f"Here is a user's spending breakdown by category: {data_str}. "
        f"Write a short, friendly 2-3 sentence summary of their spending, "
        f"mentioning the highest category and any notable pattern."
    )


def generate_spending_summary(category_summary):
    prompt_text = build_prompt(category_summary)

    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_text,
    )
    return response.text