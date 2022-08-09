import sys
import json
from pprint import pformat
try:
    import click
    from requests_html import HTMLSession
    from fake_useragent import UserAgent
    from packages.utils import (
        get_tag_data,
        find_posts_links,
        get_posts_data,
    )
except ModuleNotFoundError as e:
    print(e)
    print("Please download the required modules from requirements.txt")
    sys.exit()


@click.command()
@click.option(
    "--tag",
    prompt="Please enter a valid sub-reddit tag name.",
    help="Valid sub-reddit tag name. for example [python, webdev, announcements, funny]"
)
@click.option(
    '--tp', prompt='Enter total number of posts to scrape from 10 to 20',
    default=10,
    show_default=True,
    help='Total number of posts to scrape, 10-20.'
)
def main(tag, tp):
    """Scrape last 10-20 posts for the given subreddit"""
    click.echo("starting the script! (control+c to exit)")
    UA = UserAgent()
    SESSION = HTMLSession()
    try:
        divs = get_tag_data(tag, SESSION)
        links = find_posts_links(divs)
        posts = get_posts_data(links, SESSION, UA, tp)
        data = list(posts)
        with open(f"data/{tag}.json", "w", encoding="utf-8") as file_name:
            json.dump(data, file_name)

    except KeyboardInterrupt:
        print("Exiting!")
        sys.exit()


if __name__ == "__main__":
    main()
