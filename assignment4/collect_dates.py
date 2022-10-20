import re
from typing import Tuple

## -- Task 3 (IN3110 optional, IN4110 required) -- ##

# create array with all names of months
month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

...


def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """

    # Regex to capture days, months and years with numbers
    # year should accept a 4-digit number between at least 1000-2029
    year = r"\b[12]\d{3}\b"
    # month should accept month names or month numbers
    jan = r"\b[jJ]an(?:uary)?\b"
    feb = r"\b[fF]eb(?:ruary)?\b"
    mar = r"\b[mM]ar(?:ch)?\b"
    apr = r"\b[aA]pr(?:il)?\b"
    may = r"\b[mM]ay\b"
    jun = r"\b[jJ]une?\b"
    jul = r"\b[jJ]uly?\b"
    aug = r"\b[aA]aug(?:ust)?\b"
    sep = r"\b[sS]ep(?:tember)?\b"
    okt = r"\b[oO]ct(?:ober)?\b"
    nov = r"\b[nN]ov(?:ember)?\b"
    dec = r"\b[dD]ec(?:ember)?\b"

    decimal_month = r"\b[01]?[0-9]\b"

    month = rf"(?:{jan}|{feb}|{mar}|{apr}|{may}|{jun}|{jul}|{aug}|{sep}|{okt}|{nov}|{dec}|{decimal_month})"
    month = rf"{jan}"
    # day should be a number, which may or may not be zero-padded
    day = r"(?[0-3]?[0-9])"

    return year, month, day


def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    # If already digit do nothing
    if s.isdigit():
        return s

    # Convert to number as string
    ...


def zero_pad(n: str):
    """zero-pad a number string

    turns '2' into '02'

    You don't need to use this function,
    but you may find it useful.
    """
    return f"0{n}"


def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found
    """
    year, month, day = get_date_patterns()

    # Date on format YYYY/MM/DD - ISO
    ISO = ...

    # Date on format DD/MM/YYYY
    DMY = ...

    # Date on format MM/DD/YYYY
    MDY = ...

    # Date on format YYYY/MM/DD
    YMD = ...

    # list with all supported formats
    formats = ...
    dates = []

    # find all dates in any format in text
    ...
    # Write to file if wanted
    if output:
        ...

    return dates
