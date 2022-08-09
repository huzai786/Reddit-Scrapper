from bs4 import BeautifulSoup, Tag, NavigableString
from requests_html import HTMLSession
from fake_useragent import UserAgent
from typing import Generator, Type, Tuple, Any
from collections import namedtuple, defaultdict
import traceback
import requests
import datetime
import time
import sys
import re


def get_tag_data(reddit_tag: str, session) -> Tag:
    """Render the page and returns the selected div containing relevant data"""

    try:
        r = session.get(f"https://www.reddit.com/r/{reddit_tag}/new/")
        print("Rendering...")
        r.html.render(sleep=2, scrolldown=1, wait=2, timeout=30)
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
    current_time = datetime.datetime.now()
    time_list = time_msg.split()
    if time_list[0] == 'just':
        time_str = current_time.strftime("%d, %B, %Y %I:%p")
        return time_str
    time_sec = float(time_list[0])
    if time_list[1] == "hour":
        time_sec = time_sec * 3600
    if time_list[1] == "minutes":
        time_sec = time_sec * 60
    time = current_time - datetime.timedelta(seconds=time_sec)
    time_str = time.strftime("%d, %B, %Y %I:%p")
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
    return post_links


def _get_raw_time(time_string: str) -> int:
    time = int(datetime.datetime.strptime(
        time_string, '%d, %B, %Y %I:%p').timestamp())
    return time


def _get_links(content):
    desc_text = ''
    external_link = []
    embedded_link = []
    aas = content.find_all('a')
    for a in aas:
        if a.parent.name == 'p':
            embedded_link.append(a['href'])
        if a.parent.name == 'div':
            external_link.append(a['href'])
    external_link = list(
        set([e for e in external_link if e.startswith('https://')]))
    embedded_link = list(
        set([e for e in embedded_link if e.startswith('https://')]))
    return embedded_link, external_link


def _handle_description_scraping(desc_tag: Tag) -> str:
    desc_data_list = desc_tag.find_all("p") if desc_tag else None
    description = "description not found"
    if desc_data_list:
        description = ""
        for d in desc_data_list:
            data = re.sub(r"\s+", " ", d.get_text())
            description += data
            description += "\n"

    return description


def _data_handle(content: Tag) -> dict:
    """Handle data returned from the bs4 data extraction methods"""

    post_data = defaultdict(dict)
    try:
        # Finding data
        author = content.select_one('div > a[data-testid="post_author_link"]')
        posted_on = content.find(
            "span",
            {"data-click-id": "timestamp", "data-testid": "post_timestamp"},
        )
        title = content.find(
            'div', {'data-adclicklocation': 'title'}).find('h1')
        desc = content.select_one('div[data-click-id="text"] > div')

        # Data Filtering
        posted_on_str = _handle_time(
            posted_on.get_text()) if posted_on else None
        raw_time = _get_raw_time(posted_on_str) if posted_on_str else None
        author_str = author.get_text().replace('u/', '') if author else None
        title_str = title.get_text() if title else None
        embedded_link, external_links = _get_links(content)
        description = _handle_description_scraping(desc)

        # Adding to dictionary
        post_data["author"] = author_str
        post_data["author_link"] = f"https://www.reddit.com/user/{author_str}/"
        post_data["posted_at"] = posted_on_str
        post_data["raw_time"] = raw_time
        post_data["title"] = title_str
        post_data["description"] = description
        post_data["links"]['embedded_link'] = embedded_link
        post_data["links"]['external_links'] = external_links
        print(f"Post Author: {author_str}")

        return dict(post_data)

    except IndexError as e:
        print("Data not found!")
        print(e)


def get_posts_data(
    post_links: list, session: HTMLSession, ua: UserAgent, total_post: int
) -> Type[Generator]:
    """Returns a generator for the Posts data when iterated on each link"""

    print(f'Getting data for recent {total_post} posts!')
    for link in post_links[:total_post]:
        try:
            headers = {"user-agent": f"{ua.random}"}
            r = session.get(
                f"{link}",
                headers=headers,
            )
            r.html.render(sleep=1, scrolldown=1, wait=2, timeout=30)
            soup = BeautifulSoup(r.html.html, "lxml")
            content = soup.find("div", {"data-test-id": "post-content"})
            post_data_dict = _data_handle(content)
            post_data_dict['post_link'] = link
            yield post_data_dict

        except requests.TooManyRedirects:
            print("To many request!")
            time.sleep(5)
            pass

        except requests.RequestException:
            traceback.print_exc()
            sys.exit()
