import re

import holidays
from enum import Enum, unique, auto
from datetime import datetime, date

date_format = "%d/%m/%Y"


class Region(Enum):
    UK = 1
    ENGLAND = 2
    NORTHERN_IRELAND = 3
    SCOTLAND = 4
    WALES = 5


def check_postcode(postcode: str):
    """
    Checks a postcode exists and validates UK formatting against a RegEx string
        :param postcode: Postcode to parse
    """
    postcode_re = "^([A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]? ?[0-9][A-Za-z]{2}|[Gg][Ii][Rr] ?0[Aa]{2})$"
    try:
        if postcode is None or not re.fullmatch(postcode_re, postcode):
            raise ValueError("Invalid postcode")
        return True
    except Exception as ex:
        print(f"Exception encountered: {ex}")
        print(
            "Please check the provided postcode"
        )
        exit(1)


def check_paon(paon: str):
    """
    Checks that PAON data exists
        :param paon: PAON data to check, usually house number
    """
    try:
        if paon is None:
            raise ValueError("Invalid house number")
        return True
    except Exception as ex:
        print(f"Exception encountered: {ex}")
        print(
            "Please check the provided house number."
        )
        exit(1)


def check_uprn(uprn: str):
    """
    Checks that the UPRN exists
        :param uprn: UPRN to check
    """
    try:
        if uprn is None or uprn == "":
            raise ValueError("Invalid UPRN")
        return True
    except Exception as ex:
        print(f"Exception encountered: {ex}")
        print(
            "Please check the provided UPRN."
        )


def get_date_with_ordinal(date_number: int) -> str:
    """
    Return ordinal text on day of date
        :rtype: str
        :param date_number: Date number as an integer (e.g. 4)
        :return: Return date with ordinal suffix (e.g. 4th)
    """
    return str(date_number) + (
        "th"
        if 4 <= date_number % 100 <= 20
        else {1: "st", 2: "nd", 3: "rd"}.get(date_number % 10, "th")
    )


def parse_header(raw_header: str) -> dict:
    """
    Parses a header string and returns one that can be useful
            :rtype: dict
            :param raw_header: header as a string, with values to separate as pipe (|)
            :return: header in a dictionary format that can be used in requests
    """
    header = dict()
    for line in raw_header.split("|"):

        if line.startswith(":"):
            a, b = line[1:].split(":", 1)
            a = f":{a}"
        else:
            a, b = line.split(":", 1)

        header[a.strip()] = b.strip()

    return header


def is_holiday(date_to_check: datetime, region: Region = Region.UK) -> bool:
    """
Checks if a given date is a public holiday.
    :param date_to_check: Date to check if holiday
    :param region: The UK nation to check. Defaults to UK.
    :return: Bool - true if a holiday, false if not
    """
    uk_holidays = holidays.country_holidays('GB', subdiv=region.name)

    if date_to_check in uk_holidays:
        return True
    else:
        return False

