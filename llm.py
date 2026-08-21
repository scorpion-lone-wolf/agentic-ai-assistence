import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")


client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


def call_llm(messages, tools=None):
    """
    Send messages to Gemini.

    We return the complete assistant message because
    it may contain either:

    1. normal text
    2. tool calls
    """

    response = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=messages,
        tools=tools,
    )

    return response.choices[0].message
