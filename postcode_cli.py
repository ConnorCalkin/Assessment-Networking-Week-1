"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import validate_postcode


def get_args():
    parser = ArgumentParser()
    parser.add_argument('postcode')
    parser.add_argument(
        '--mode', "-m", choices=["validate", "complete"], required=True)
    return parser.parse_args()


def output_validate_postcode(postcode: str) -> None:
    if validate_postcode(postcode) is True:
        print(f'{postcode} is a valid postcode.')
    else:
        print(f'{postcode} is not a valid postcode.')


if __name__ == "__main__":
    args = get_args()
    postcode = args.postcode
    postcode = postcode.upper().strip()
    if args.mode == "validate":
        output_validate_postcode(postcode)
    if args.mode == "complete":
        pass
