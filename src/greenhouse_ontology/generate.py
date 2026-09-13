import os
from pathlib import Path

from google import genai


DEFAULT_MODEL = "gemini-3.8-flash"


def load_prompt(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8").strip()


def generate(
    prompt_path: str | Path,
    output_dir: str | Path,
    model: str = DEFAULT_MODEL,
) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    prompt = load_prompt(prompt_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = genai.Client(api_key=api_key)
    try:
        interaction = client.interactions.create(model=model, input=prompt)
        response = interaction.output_text

        if response is None:
            raise RuntimeError("Gemini returned no text")

        (output_dir / "response.txt").write_text(response, encoding="utf-8")
        return response
    finally:
        client.close()
