import sys
from pathlib import Path

from rdflib import Graph

from greenhouse_ontology.extract_ttl import extract_ttl
from greenhouse_ontology.generate import DEFAULT_MODEL, generate
from greenhouse_ontology.validate import validate

def run_pipeline(
    prompt_path: str | Path,
    output_dir: str | Path,
    model: str = DEFAULT_MODEL,
) -> Graph:
    output_dir = Path(output_dir)
    response_path = output_dir / "response.txt"
    ontology_path = output_dir / "ontology.ttl"

    print("Generating LLM output to prompt...")
    generate(prompt_path, output_dir, model)

    print("Extracting output into ttl file")
    extract_ttl(response_path, ontology_path)

    return validate(ontology_path)

def main() -> None:
    if len(sys.argv) not in {3, 4}:
        raise SystemExit(
            "Usage: python -m greenhouse_ontology.pipeline "
            "PROMPT OUTPUT_DIR [MODEL]"
        )

    model = sys.argv[3] if len(sys.argv) == 4 else DEFAULT_MODEL
    graph = run_pipeline(sys.argv[1], sys.argv[2], model)
    print(f"Valid Turtle ontology ({len(graph)} triples)")

if __name__ == "__main__":
    main()
