import sys
from pathlib import Path

import semchunk

def main(input_path):
    input_path = Path(input_path)

    text = input_path.read_text(encoding="utf-8")
    chunker = semchunk.chunkerify("o200k_base", 4_000)
    print(chunker(text))

if __name__ == '__main__':
    main(sys.argv[1])