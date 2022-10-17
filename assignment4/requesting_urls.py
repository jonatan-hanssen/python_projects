from typing import Dict, Optional

import requests

## -- Task 1 -- ##


def get_html(url: str, params: Optional[Dict] = None, output: Optional[str] = None):
    """Get an HTML page and return its contents.

    Args:
        url (str):
            The URL to retrieve.
        params (dict, optional):
            URL parameters to add.
        output (str, optional):
            (optional) path where output should be saved.
    Returns:
        html (str):
            The HTML of the page, as text.
    """
    # passing the optional parameters argument to the get function
    response = requests.get(url, params=params)

    html_str = response.text

    if output:
        # if output is specified, the response txt and url get printed to a
        # txt file with the name in `output`

        # I will do no checking to see if it is a .txt file. You should be able to write to any file
        # you want. File extensions dont really matter unless you want to double click the file instead of
        # opening it in the terminal.
        with open(output, "w") as file:
            file.write(f"HTTP GET request at {response.url}:\n{response.text}")

    return html_str


get_html("https://nrk.no", output="snake")
