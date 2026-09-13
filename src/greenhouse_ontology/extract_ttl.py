from pathlib import Path


def remove_fence(text: str) -> str:
    lines = text.splitlines()

    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    if lines and lines[0].strip().lower() in {"```", "```turtle", "```ttl"}:
        lines.pop(0)

        if not lines or lines[-1].strip() != "```":
            raise ValueError("Turtle code block has no closing fence")

        lines.pop()

    turtle = "\n".join(lines).strip()
    return f"{turtle}\n" if turtle else ""


def extract_ttl(input_path: str | Path, output_path: str | Path) -> str:
    input_path = Path(input_path)
    output_path = Path(output_path)

    if input_path.suffix.lower() != ".txt":
        raise ValueError("Input must be a .txt file")
    if output_path.suffix.lower() != ".ttl":
        raise ValueError("Output must be a .ttl file")

    turtle = remove_fence(input_path.read_text(encoding="utf-8"))
    if not turtle:
        raise ValueError("Response contains no Turtle content")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(turtle, encoding="utf-8")

    return turtle
