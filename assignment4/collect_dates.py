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
    # day should be a number, which may or may not be zero-padded
    day = r"(?:[0-3]?[0-9])"

    return year, month, day


def convert_date(s: str) -> str:
    """Converts a date without zero padding and with typed months into a date with
    padding and numeric months. (e.g. 'January 5, 2020' -> '01 05, 2020'

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """

    month_list = [
        r"\b[jJ]an(?:uary)?\b",
        r"\b[fF]eb(?:ruary)?\b",
        r"\b[mM]ar(?:ch)?\b",
        r"\b[aA]pr(?:il)?\b",
        r"\b[mM]ay\b",
        r"\b[jJ]une?\b",
        r"\b[jJ]uly?\b",
        r"\b[aA]aug(?:ust)?\b",
        r"\b[sS]ep(?:tember)?\b",
        r"\b[oO]ct(?:ober)?\b",
        r"\b[nN]ov(?:ember)?\b",
        r"\b[dD]ec(?:ember)?\b",
    ]

    # there are probably more effective ways than looping over
    # every possible pattern
    for i in range(len(month_list)):
        s = re.sub(month_list[i], str(i + 1), s)

    # zero pad any singular digits. this fixes both the months
    # created above and any non-zero-padded days in the date also
    s = re.sub(r"\b([0-9])\b", r"0\1", s)

    return s


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
        ...

    # Convert to number as string
    ...


def zero_pad(n: str):
    """zero-pad a number string
    turns '2' into '02'
    You don't need to use this function,
    but you may find it useful.
    """
    ...


def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found
    """
    year, month, day = get_date_patterns()

    # Date on format YYYY/MM/DD - ISO
    ISO = rf"{year}\W[01][0-9]\W[0-3][0-9]"

    # Date on format DD/MM/YYYY
    DMY = rf"{day}\W+{month}\W+{year}"

    # Date on format MM/DD/YYYY
    MDY = rf"{month}\W+{day}\W+{year}"

    # Date on format YYYY/MM/DD
    YMD = rf"{year}\W+{month}\W+{day}"

    # list with all supported formats
    format_dict = {"iso": ISO, "dmy": DMY, "mdy": MDY, "ymd": YMD}

    # find all dates in any format in text
    dates = list()

    for key in format_dict:

        matches_list = list()

        # we use iter because we need info about where the match was found
        for match_obj in re.finditer(format_dict[key], text):
            matches_list.append((match_obj.span()[0], match_obj.group(0)))

        for i in range(len(matches_list)):
            matches_list[i] = (matches_list[i][0], convert_date(matches_list[i][1]))

            if key == "iso":
                matches_list[i] = (
                    matches_list[i][0],
                    re.sub(
                        r"(\d{4})\W+(\d{2})\W+(\d{2})", r"\1/\2/\3", matches_list[i][1]
                    ),
                )

            if key == "dmy":
                matches_list[i] = (
                    matches_list[i][0],
                    re.sub(
                        r"(\d{2})\W+(\d{2})\W+(\d{4})", r"\3/\2/\1", matches_list[i][1]
                    ),
                )

            if key == "mdy":
                matches_list[i] = (
                    matches_list[i][0],
                    re.sub(
                        r"(\d{2})\W+(\d{2})\W+(\d{4})",
                        r"\3/\1/\2",
                        matches_list[i][1],
                    ),
                )

            if key == "ymd":
                matches_list[i] = (
                    matches_list[i][0],
                    re.sub(
                        r"(\d{4})\W+(\d{2})\W+(\d{2})", r"\1/\2/\3", matches_list[i][1]
                    ),
                )
        dates.extend(matches_list)

    # we now need to remove duplicates in case something matches
    # for both iso and ymd. Casting to a set does this. This does not remove
    # the same date if it appears twice, only if we had two matches at the exact same
    # place. We cast right back to a list afterwards
    dates = list(set(dates))

    # the default implementation is to sort based on the first element in a tuple,
    # so we are good
    dates.sort()

    # but we only care about the second element
    dates = [dates[i][1] for i in range(len(dates))]

    # Write to file if wanted
    if output:
        with open(output, "w") as file:
            text = ""
            for date in dates:
                text += f"{date}\n"
            file.write(text)

    return dates
