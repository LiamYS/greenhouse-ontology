import sys
from pathlib import Path
import ollama

import semchunk

def chunk(input_path):
    input_path = Path(input_path)
    text = input_path.read_text(encoding="utf-8")
    chunker = semchunk.chunkerify("o200k_base", 4_000)
    return chunker(text)

def process_with_ollama(chunks, system_prompt, model = "ministral-3:3b"):
    responses = []

    for i, chunk in enumerate(chunks):
        prompt = f"[Chunk {i+1} of {len(chunks)}]\n\n{chunk}"

        try:
            result = ollama.generate(model = model, prompt = prompt, system = system_prompt)
            response = result.response
            responses.append(response)
            print(f"Processed chunk {i+1}/{len(chunks)}")
        except ollama.ResponseError as e:
            print("Error: ", e.error)

    return responses


def main():
    chunks = chunk('greenhouse_technology_management.txt')

    system_prompt = """
    You are analyzing a document that has been divided into chunks.
    For each chunk:
    1. Extract an ontology in TTL format from the following text. Only return the created TTL code. Make sure to label all classes as `rdfs:Class`, all individuals as `owl:NamedIndividual`, and all properties as `owl:ObjectProperty`, `owl:DatatypeProperty`, or `owl:AnnotationProperty`.
    2. Note how these connect to previous chunks if applicable.
    3. Maintain a coherent understanding of the document as it progresses.
    """

    print("Processing chunks with Ollama...")
    chunk_analyses = process_with_ollama(chunks, system_prompt)

    print(chunk_analyses)

if __name__ == '__main__':
    main()