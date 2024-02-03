import argparse
from contextlib import nullcontext
from pathlib import Path
import shelve

from . import translate_directory, translate_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Translates website assets.")
    parser.add_argument(
        "-i", "--input", type=Path, required=True, help="Input file or directory"
    )
    parser.add_argument(
        "-o", "--output", type=Path, required=True, help="Output file or directory"
    )
    parser.add_argument("-c", "--cache", type=Path, help="Translation cache directory")
    parser.add_argument(
        "--source-language", type=str, required=True, help="Source language"
    )
    parser.add_argument(
        "--target-language", type=str, required=True, help="Target language"
    )
    args = parser.parse_args()

    cache_context = nullcontext({})
    if args.cache:
        cache_context = shelve.open(args.cache / args.target_language)
    with cache_context as cache:
        if args.input.is_file():
            translate_file(
                args.input,
                args.output,
                args.source_language,
                args.target_language,
                cache,
            )
        else:
            translate_directory(
                args.input,
                args.output,
                args.source_language,
                args.target_language,
                cache,
            )


if __name__ == "__main__":
    main()
