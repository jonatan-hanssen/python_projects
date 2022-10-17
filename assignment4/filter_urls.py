import re
from urllib.parse import urljoin

## -- Task 2 -- ##


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex
    Arguments:
        html (str): html string to parse
    Returns:
        urls (set) : set with all the urls found in html text
    """
    # create and compile regular expression(s)

    url_pat = r"<a .*href=[\"']([^#'\"]+)[#\"'].*<\/a>"

    # url_pat = re.compile(pattern)

    urls = re.findall(url_pat, html)
    # additional processing to change path urls to full urls

    # urls_string = " ".join(urls)
    # print(urls_string)

    # 1. find all the anchor tags, then
    # 2. find the urls href attributes

    # add base_url to relative paths and https to those with same protocol
    for i in range(len(urls)):
        if len(urls[i]) < 2:
            continue

        if urls[i][0] == "/":
            if urls[i][1] != "/":
                urls[i] = base_url + urls[i]
            else:
                urls[i] = "https:" + urls[i]

    urls = set(urls)

    # Write to file if requested
    if output:
        print(f"Writing to: {output}")
        with open(output, "w") as file:
            # join the urls with space as separator. then replace space with newline,
            # and write this to output
            file.write(re.sub(r"\s", "\n", " ".join(urls)))

    return urls


def find_articles(html: str, output=None) -> set:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """
    urls = find_urls(html)
    pattern = r"(https:\/\/[a-z]{2}\.wikipedia\.org\/wiki\/[^:\s]+)"
    articles = re.findall(pattern, " ".join(urls))

    articles = set(articles)
    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        with open(output, "w") as file:
            # join the urls with space as separator. then replace space with newline,
            # and write this to output
            file.write(re.sub(r"\s", "\n", " ".join(articles)))

    return articles


## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        src = src_pat.find(img_tag)
        src_set.add(src)
    return src_set
