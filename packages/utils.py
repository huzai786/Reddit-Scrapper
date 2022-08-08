from bs4 import BeautifulSoup, Tag, NavigableString
from requests_html import HTMLSession
from fake_useragent import UserAgent
from typing import Generator, Type, Tuple, Any
from collections import namedtuple
import traceback
import requests
import datetime
import time
import sys


def get_tag_data(reddit_tag: str, session) -> Tag:
    """Render the page and returns the selected div containing relevant data"""

    try:
        r = session.get(f"https://www.reddit.com/r/{reddit_tag}/new/")
        print("Rendering...")
        r.html.render(sleep=2, scrolldown=1, wait=3, timeout=30)
        soup = BeautifulSoup(r.html.html, "lxml")
        divs = soup.select("div > div#AppRouter-main-content")[0]
        return divs

    except Exception:
        traceback.print_exc()
        print("Exiting...")
        sys.exit()


def _extract_link(tag: Tag) -> str:
    try:
        atag = tag.find("a", {"data-click-id": "body"})
        if atag is not None:
            link = "https://www.reddit.com" + atag["href"]
            return link

    except Exception:
        print("Link not found!")
        return ""


def _handle_time(time_msg: str) -> str:
    time_list = time_msg.split()
    time_sec = float(time_list[0])
    if time_list[1] == "hour":
        time_sec = time_sec * 3600
    if time_list[1] == "minutes":
        time_sec = time_sec * 60
    time = datetime.datetime.now() - datetime.timedelta(seconds=time_sec)
    time_str = time.strftime("%y:%M:%d %I:%M")
    return time_str


def find_posts_links(Bs4Tag: Tag) -> Tag:
    """Finds all the 'Posts' Links on the page and returns then as list"""

    post_links = []
    if Bs4Tag is not None:
        divs = Bs4Tag.find_all("div", {"data-testid": "post-container"})
        for div in divs:
            span = div.find("span", string="promoted")
            if span is None:
                link = _extract_link(div)
                if link != "":
                    post_links.append(link)
    print(f"{len(post_links)} Links found!")
    return post_links


def _data_handle(values_tags: Type[Tuple[Any, ...]]) -> dict:
    post_data = {}
    description = ""
    if desc != []:
        for d in desc:
            description += d.get_text()
            description += "\n"
    if time is not None:
        time_str = _handle_time(time.get_text())
    if user is not None:
        user_str = user.get_text()
    if title is not None:
        title_str = title.get_text()
    if description == "":
        description = "description not found"

    post_data["author"] = user_str
    post_data["posted_at"] = time_str
    post_data["title"] = title_str
    post_data["description"] = description
    print(f"Post Author: {user_str}")
    pass


def get_posts_data(
    post_links: list, session: HTMLSession, ua: UserAgent) -> Type[Generator]:
    """Returns a generator for the Posts data when iterated on each link"""

    for link in post_links[:10]:
        try:
            headers = {"user-agent": f"{ua.random}"}
            r = session.get(
                f"{link}",
                headers=headers,
            )
            r.html.render(sleep=1, scrolldown=1, wait=3, timeout=30)
            soup = BeautifulSoup(r.html.html, "lxml")
            content = soup.find("div", {"data-test-id": "post-content"})
            posted_on = content.find(
                "span",
                {"data-click-id": "timestamp", "data-testid": "post_timestamp"},
            )
            author = content.select_one('div > a[data-testid="post_author_link"]')
            title = content.select_one(
                'div[data-adclicklocation="title"] > div > div > h1'
            )
            desc = content.select('div[data-click-id="text"] > div')[0]
            desc = desc.find_all("p")
            postDataObjects = namedtuple('post_data_object', ['author', 'posted_on', 'title', 'description'])
            post_data_variables = postDataObjects(author=author, posted_on=posted_on, title=title, description=desc)
            post_data_dict = _data_handle(post_data_variables)

            yield post_data_dict

        except IndexError:
            print("Value Not Found!")
            return {}

        except requests.TooManyRedirects:
            print("To many request!")
            time.sleep(5)
            pass

        except requests.RequestException:
            traceback.print_exc()
            sys.exit()
