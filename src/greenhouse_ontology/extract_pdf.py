from pathlib import Path
import sys
import pymupdf4llm

def main(input_path: str | Path, output_path: str | Path):
    text = pymupdf4llm.to_text(input_path)
    Path(output_path).write_text(text, encoding="utf-8")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
