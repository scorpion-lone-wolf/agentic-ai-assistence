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

    Returns the complete assistant message because it may contain:
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

            return response.choices[0].message

        except openai.APITimeoutError as error:

            print(f"[LLM Error] : Timeout error: {error}")

            if attempt == MAX_LLM_RETRY:
                raise

            should_retry = True

        except openai.RateLimitError as error:

            print(f"[LLM Error] : Rate limit error: {error}")

            if attempt == MAX_LLM_RETRY:
                raise

            should_retry = True

        except openai.APIConnectionError as error:

            print(f"[LLM Error] : Connection error: {error}")

            if attempt == MAX_LLM_RETRY:
                raise

            should_retry = True

        except openai.APIStatusError as error:

            print(f"[LLM Error] : API status {error.status_code}: " f"{error}")

            if error.status_code >= 500:

                if attempt == MAX_LLM_RETRY:
                    raise

                should_retry = True

            else:
                # 4xx errors are normally not retryable.
                raise

        # Only retry when execution reaches this point.
        if should_retry:

            delay = INITIAL_RETRY_DELAY * (2**attempt)

            print(f"[LLM Error] : " f"Retrying after {delay} seconds...")

            time.sleep(delay)


def call_llm_text(messages):
    """
    Call the LLM without tools and return only text.
    """
    message = call_llm(messages)
    return message.content
