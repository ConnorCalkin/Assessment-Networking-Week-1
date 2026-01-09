"""Functions that interact with the Postcode API."""

import json
import requests as req


CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("AAA")
        return {}


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    json_str = json.dumps(cache, indent=4)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(json_str)


def add_cache_valid(postcode: str, valid: bool) -> None:
    '''adds the valid value to the postcode in the cache'''
    cache = load_cache()
    if postcode not in cache:
        cache[postcode] = {}
    cache[postcode]["valid"] = valid
    save_cache(cache)


def add_cache_completions(postcode: str, completions: list[str]) -> None:
    '''adds the completions to the postcode in the cache'''
    cache = load_cache()
    if postcode not in cache:
        cache[postcode] = {}
    cache[postcode]["completions"] = completions
    save_cache(cache)


def get_validate_url(postcode: str):
    '''gives the url for the validate endpoint'''
    return f"https://api.postcodes.io/postcodes/{postcode}/validate"


def get_location_url(lon: float, lat: float):
    '''gives the url for the latitude, longitude endpoint'''
    return f"https://api.postcodes.io/postcodes?lon={lon}&lat={lat}"


def get_collections_url(postcode_start: str):
    '''gives the url for the autocomplete endpoint'''
    return f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete"


def get_details_url():
    '''gives the url for getting the postcode details from a bulk request'''
    return "https://api.postcodes.io/postcodes"


def validate_postcode_from_api(postcode: str) -> bool:
    '''gets whether the postcode is valid by accessing the API'''
    response = req.get(get_validate_url(postcode), timeout=10)
    if response.status_code != 200:
        raise req.RequestException("Unable to access API.")

    return response.json()["result"]


def validate_postcode_from_cache(postcode: str) -> bool:
    '''
    gets whether the postcode is valid from the cache
    if it can't find it, it will return a RunTimeError
    '''
    cache = load_cache()
    try:
        return cache[postcode]["valid"]
    except KeyError as e:
        raise RuntimeError(f"No value for postcode {postcode} in cache") from e


def validate_postcode(postcode: str) -> bool:
    '''
    returns whether a postcode is a valid postcode or not
    '''
    if isinstance(postcode, str) is False:
        raise TypeError("Function expects a string.")

    try:
        return validate_postcode_from_cache(postcode)
    except RuntimeError:
        valid = validate_postcode_from_api(postcode)
        add_cache_valid(postcode, valid)
        return valid


def get_postcode_for_location(lat: float, long: float) -> str:
    '''
    uses a location given by their longitude and latitude
    and returns the corresponding postcode
    '''
    if isinstance(lat, float) is False or isinstance(long, float) is False:
        raise TypeError("Function expects two floats.")

    response = req.get(get_location_url(long, lat), timeout=10)

    if response.status_code != 200:
        raise req.RequestException("Unable to access API.")

    result = response.json()["result"]
    if result is None:
        raise ValueError("No relevant postcode found.")

    return result[0]["postcode"]


def get_postcode_completions_from_api(postcode_start: str) -> list[str]:
    '''Gets the completions of the postcode from the API'''
    response = req.get(get_collections_url(postcode_start), timeout=10)
    if response.status_code != 200:
        raise req.RequestException("Unable to access API.")

    response_json = response.json()
    if response_json["result"] is None:
        raise ValueError("No relevant postcode found.")

    return response_json["result"]


def get_postcode_completions_from_cache(postcode_start: str) -> list[str]:
    '''gets the completions of the postcodes from the cache'''
    cache = load_cache()
    try:
        return cache[postcode_start]["completions"]
    except KeyError as e:
        raise RuntimeError(
            f"No collections value for {postcode_start} in cache") from e


def get_postcode_completions(postcode_start: str) -> list[str]:
    '''
    gets the postcodes that start with a certain value
    '''
    if isinstance(postcode_start, str) is False:
        raise TypeError("Function expects a string.")

    try:
        return get_postcode_completions_from_cache(postcode_start)
    except RuntimeError:
        completions = get_postcode_completions_from_api(postcode_start)
        add_cache_completions(postcode_start, completions)
        return completions


def get_postcodes_details(postcodes: list[str]) -> dict:
    '''
    given a list of postcodes, this does a bulk api call, and returns
    the API data for each of them
    '''
    if isinstance(postcodes, list) is False:
        raise TypeError("Function expects a list of strings.")
    if any(isinstance(postcode, str) is False for postcode in postcodes):
        raise TypeError("Function expects a list of strings.")

    request_json = {
        "postcodes": postcodes
    }
    response = req.post(get_details_url(postcodes),
                        json=request_json, timeout=10)

    if response.status_code != 200:
        raise req.RequestException("Unable to access API.")

    response_json = response.json()
    results = response_json["result"]

    if results is None:
        raise ValueError("No relevant postcode found.")

    return results
