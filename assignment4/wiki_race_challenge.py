from typing import List  # isort:skip
from requesting_urls import get_html
from filter_urls import find_articles
import re


def find_path(start: str, finish: str) -> List[str]:
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

    queue = [Node(start, None)]

    while queue:
        node = queue.pop(0)
        only_article_pattern = r"\/wiki\/(.*)"
        match = re.search(only_article_pattern, node.url)
        only_article = match.group(1)
        print(
            f"Articles found: {len(queue)} | Layer: {node.layer} | Article: {only_article}"
        )
        if node.url == finish:
            break
        html = get_html(node.url)
        articles = find_articles(html)
        node_list = [Node(url, node) for url in articles]
        queue.extend(node_list)
        if len(queue) == 0:
            print("No path found")
            exit()

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
    start = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    finish = "https://en.wikipedia.org/wiki/Peace"

    path = find_path(start, finish)
    print(path)
