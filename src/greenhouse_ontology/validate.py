from pathlib import Path

from rdflib import Graph


def validate(path: str | Path) -> Graph:
    path = Path(path)

    if path.suffix.lower() != ".ttl":
        raise ValueError("Ontology must be a .ttl file")

    turtle = path.read_text(encoding="utf-8")
    if not turtle.strip():
        raise ValueError("Ontology contains no Turtle content")

    graph = Graph()
    try:
        graph.parse(data=turtle, format="turtle")
    except Exception as error:
        raise ValueError(f"Invalid Turtle in {path}: {error}") from error

    if not graph:
        raise ValueError("Ontology contains no RDF triples")

    return graph
