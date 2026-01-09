"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.
    ...


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    # This function is used in Task 3, you can ignore it for now.
    ...


def get_validate_url(postcode: str):
    '''gives the url for the validate endpoint'''
    return f"https://api.postcodes.io/postcodes/{postcode}/validate"


def get_location_url(lon: float, lat: float):
    '''gives the url for the latitude, longitude endpoint'''
    return f"https://api.postcodes.io/postcodes?lon={lon}&lat={lat}"


def get_collections_url(postcode_start: str):
    '''gives the url for the autocomplete endpoint'''
    return f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete"


def get_details_url(postcodes: list[str]):
    return "https://api.postcodes.io/postcodes"


def validate_postcode(postcode: str) -> bool:
    if isinstance(postcode, str) is False:
        raise TypeError("Function expects a string.")

    response = req.get(get_validate_url(postcode))
    if response.status_code != 200:
        raise req.RequestException("Unable to access API.")

    return response.json()["result"]


def get_postcode_for_location(lat: float, long: float) -> str:
    if isinstance(lat, float) is False or isinstance(long, float) is False:
        raise TypeError("Function expects two floats.")

    response = req.get(get_location_url(long, lat))

    if response.status_code != 200:
        raise req.RequestException("Unable to access API.")

    result = response.json()["result"]
    if result is None:
        raise ValueError("No relevant postcode found.")

    return result[0]["postcode"]


def get_postcode_completions(postcode_start: str) -> list[str]:
    if isinstance(postcode_start, str) is False:
        raise TypeError("Function expects a string.")

    response = req.get(get_collections_url(postcode_start))
    if response.status_code != 200:
        raise req.RequestException("Unable to access API.")

    json = response.json()
    if json["result"] is None:
        raise ValueError("No relevant postcode found.")

    return json["result"]


def get_postcodes_details(postcodes: list[str]) -> dict:
    if isinstance(postcodes, list[str]) is False:
        raise TypeError("Function expects a list of strings.")

    response = req.get(get_details_url(postcodes))
