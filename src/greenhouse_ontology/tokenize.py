import argparse
from pathlib import Path

import tiktoken

def main(input_path: str | Path) -> None:
    text = Path(input_path).read_text(encoding="utf-8")
    # encoding = tiktoken.get_encoding("o200k_base")
    encoding = tiktoken.encoding_for_model('gpt-4-mini')
    token_count = len(encoding.encode(text))

    print(token_count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count tokens in a text file.")
    parser.add_argument("input_path", type=Path, help="Path to the input text file")
    args = parser.parse_args()

    main(args.input_path)
