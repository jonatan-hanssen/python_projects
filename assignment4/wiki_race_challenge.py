from typing import List  # isort:skip
from requesting_urls import get_html
from filter_urls import find_articles
import re
import sys
import argparse


def find_path(start: str, finish: str, no_print=False) -> List[str]:
    """Find the shortest path from `start` to `finish`

    Arguments:
      start (str): wikipedia article URL to start from
      finish (str): wikipedia article URL to stop at

    Returns:
      urls (list[str]):
        List of URLs representing the path from `start` to `finish`.
        The first item should be `start`.
        The last item should be `finish`.
        All items of the list should be URLs for wikipedia articles.
        Each article should have a direct link to the next article in the list.
    """

    # we will use BFS, as this will give us the shortest path

    class Node:
        """tiny class for storing previous urls so that we can trace back the path
        parameters:
            url (string): an url to a wikipedia article
            parent (Node): the node of the url which led us to the url in this node
        """

        def __init__(self, url, parent):
            self.url = url
            self.parent = parent
            if parent == None:
                self.layer = 0
            else:
                self.layer = parent.layer + 1

    match = re.match(r"https:\/\/[a-z]{2}\.wikipedia\.org", start)
    # here we just assume that there are no links to wikipedia in other languages
    base_url = match.group()

    # we cannot use a list because we do not want duplicates and do not want to check
    # for them as that is costly. We cannot use sets as two nodes with the same
    # url are still different objects. So we use dictionaries and urls as keys.
    # This means we are overwriting if we find the same url twice, but it does not
    # matter as overwriting will only happen on the same layer, which is irrelevant
    # for finding the shortest path
    cur_layer = {start: Node(start, None)}
    next_layer = {}

    # used for printing on the same line
    print_string = ""

    # bfs loop
    while True:
        # pop an element from the current layer
        node = cur_layer.popitem()[1]
        # grab only the article
        only_article_pattern = r"\/wiki\/(.*)"
        match = re.search(only_article_pattern, node.url)
        # truncate at 30 chars for prettier prints
        only_article = match.group(1)[:30]

        if not no_print:
            print(" " * len(print_string), end="\r")
            print_string = f"  Nodes in layer {node.layer}: {len(cur_layer)}. Nodes in layer {node.layer + 1}: {len(next_layer)} | Article: {only_article}"
            print(
                print_string,
                end="\r",
            )

        html = get_html(node.url)
        articles = find_articles(html, base_url)

        if finish in articles:
            parent = node
            node = Node(finish, parent)
            break

        for url in articles:
            next_layer[url] = Node(url, node)

        if len(cur_layer) == 0:
            if len(next_layer) == 0:
                print("Ran out of urls, no path found.")
                exit()
            cur_layer = next_layer
            next_layer = {}

    path = list()

    # trace back to start
    while node.parent:
        path.insert(0, node.url)
        node = node.parent

    # we broke the while loop while on the first node, so we must append its
    # url aswell to get the start
    path.insert(0, node.url)

    assert path[0] == start
    assert path[-1] == finish
    return path


if __name__ == "__main__":

    argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Find shortest path")

    group = parser.add_mutually_exclusive_group()

    parser.add_argument(
        "-d",
        "--debug",
        help="Run with shorter path",
        action="store_true",
    )
    parser.add_argument(
        "-np",
        "--noprint",
        help="Do not print, for performance benefits",
        action="store_true",
    )

    args = parser.parse_args()

    if args.debug:
        start = "https://no.wikipedia.org/wiki/Lactobacillus"
        finish = "https://no.wikipedia.org/wiki/Melkesyre"
    else:
        start = "https://en.wikipedia.org/wiki/Python_(programming_language)"
        finish = "https://en.wikipedia.org/wiki/Peace"

    path = find_path(start, finish, no_print=args.noprint)
    print(path)
