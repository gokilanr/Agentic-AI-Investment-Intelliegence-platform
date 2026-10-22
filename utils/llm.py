
import os
import time

from dotenv import load_dotenv
from google import genai

from config.settings import BASE_DIR
from utils.logger import get_logger

load_dotenv(BASE_DIR / ".env")

logger = get_logger(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("LLM_MODEL", "gemini-3.8-flash")
MAX_RETRIES = int(os.getenv("LLM_MAX_RETRIES", "2"))

_client = None


def get_client():
    """Create the Gemini client when first needed."""
    global _client

    if _client is None:
        if not API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Check your .env file."
            )

        _client = genai.Client(api_key=API_KEY)

    return _client


def _extract_text(response) -> str:
    """Extract generated text from an Interactions API response."""
    output_text = getattr(response, "output_text", None)

    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    parts = []

    for step in getattr(response, "steps", None) or []:
        if getattr(step, "type", None) != "model_output":
            continue

        for item in getattr(step, "content", None) or []:
            item_text = getattr(item, "text", None)

            if item_text:
                parts.append(item_text)

    if parts:
        return "\n".join(parts).strip()

    raise RuntimeError(
        "Gemini returned no text. "
        f"Response status: {getattr(response, 'status', None)}"
    )


def generate_text(
    prompt: str,
    temperature: float = 0.2,
) -> str:
    """Generate text through Google's Interactions API."""
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    client = get_client()
    last_error = None

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.interactions.create(
                model=MODEL,
                input=prompt,
                generation_config={
                    "temperature": temperature,
                },
            )

            return _extract_text(response)

        except Exception as exc:
            last_error = exc

            logger.warning(
                "Gemini request failed (attempt %s/%s): %s",
                attempt + 1,
                MAX_RETRIES + 1,
                exc,
            )

            message = str(exc)
            transient = any(
                marker in message
                for marker in (
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED",
                    "500",
                    "INTERNAL",
                )
            )

            if not transient or attempt >= MAX_RETRIES:
                break

            time.sleep(2 ** attempt)

    raise RuntimeError(
        f"LLM request failed for model '{MODEL}': {last_error}"
    ) from last_error
