"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import validate_postcode, get_postcode_completions


def get_args():
    '''gets and parses the command line arguments'''
    parser = ArgumentParser()
    parser.add_argument(
        '--mode', "-m", choices=["validate", "complete"], required=True,
        help="Required string argument (validate / complete) that allows you "
        "to choose what to do")
    parser.add_argument(
        'postcode', help="Required string argument for postcode to be checked")
    return parser.parse_args()


def output_validate_postcode(postcode: str) -> None:
    '''outputs whether the code is valid according to the API'''
    if validate_postcode(postcode) is True:
        print(f'{postcode} is a valid postcode.')
    else:
        print(f'{postcode} is not a valid postcode.')


def output_completed_postcodes(postcode_start: str) -> None:
    '''outputs the completed codes obtained from the API'''
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
