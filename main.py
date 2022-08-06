import json
import time
import argparse
from requests_html import HTMLSession
from fake_useragent import UserAgent
from packages.utils import (
    get_tag_data,
    get_post_link,
    find_posts_links,
    data_handler,
    post_data,
)


def main():
    ua = UserAgent()
    session = HTMLSession()
    tag = "Python"
    divs = get_tag_data(tag, session)
    links = find_posts_links(divs)
    posts = get_posts_data(links, session, ua)
    data = []
    for p in posts:
        time.sleep(1)
        data.append(p)

    with open(f"{tag}.json", "w", encoding="utf-8") as f:
        json.dumps(data, f)


if __name__ == "__main__":
    main()
