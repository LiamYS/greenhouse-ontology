import os
from pathlib import Path
import ollama

DEFAULT_MODEL = "ministral-3:3b"

def load_prompt(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8").strip()

def generate(
    prompt_path: str | Path,
    output_dir: str | Path,
    model: str = DEFAULT_MODEL,
) -> str:

    prompt = load_prompt(prompt_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        content = ""
        interaction = ollama.generate(model=model, prompt=prompt, stream=True)

        for chunk in interaction:
            print(chunk.response, end="", flush=True)
            content += chunk.response

        (output_dir / "response.txt").write_text(content, encoding="utf-8")
        return content
    except ollama.ResponseError as e:
        print('Error: ', e.error)
