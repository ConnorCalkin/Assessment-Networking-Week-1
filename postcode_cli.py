"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import validate_postcode, get_postcode_completions


def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        '--mode', "-m", choices=["validate", "complete"], required=True)
    parser.add_argument('postcode')
    return parser.parse_args()


def output_validate_postcode(postcode: str) -> None:
    if validate_postcode(postcode) is True:
        print(f'{postcode} is a valid postcode.')
    else:
        print(f'{postcode} is not a valid postcode.')


def output_completed_postcodes(postcode_start: str) -> None:
    try:
        completions = get_postcode_completions(postcode_start)
        first_5 = completions[:5]
        for completion in first_5:
            print(completion)
    except ValueError:
        print(f'No matches for {postcode_start}.')


if __name__ == "__main__":
    args = get_args()
    postcode = args.postcode
    postcode = postcode.upper().strip()
    if args.mode == "validate":
        output_validate_postcode(postcode)
    if args.mode == "complete":
        output_completed_postcodes(postcode)
