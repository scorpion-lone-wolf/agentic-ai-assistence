import os

from dotenv import load_dotenv
from openai import OpenAI
import openai
import time

load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")
MAX_LLM_RETRY = 3
INITIAL_RETRY_DELAY = 1.0  # how many second to wait between retries


if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")


client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=20.0,
    max_retries=0,
)


def call_llm(messages, tools=None):
    """
    Send messages to Gemini.

    We return the complete assistant message because
    it may contain either:

    1. normal text
    2. tool calls
    """
    for attempt in range(MAX_LLM_RETRY + 1):
        try:
            response = client.chat.completions.create(
                model="gemini-3.1-flash-lite",
                messages=messages,
                tools=tools,
            )
        except openai.APITimeoutError as error:
            print(f"[LLM Error] : Timeout error: {error}")
            should_retry = True
        except openai.RateLimitError as error:
            print(f"[LLM Error] : Rate limit error: {error}")
            should_retry = True
        except openai.APIConnectionError as error:
            print(f"[LLM Error] : Connection error: {error}")
            should_retry = True
        except openai.APIStatusError as error:
            if error.status_code >= 500:
                should_retry = True
            else:
                should_retry = False
        # Stop immediately for non-retryable errors
        if not should_retry:
            raise

        if attempt == MAX_LLM_RETRY:
            # explicitly raise the error for maximum retry reached
            raise
        # exponential backoff
        delay = INITIAL_RETRY_DELAY * (2**attempt)
        print(f"[LLM Error] : Retrying after {delay} seconds...")

        time.sleep(delay)
    return response.choices[0].message
