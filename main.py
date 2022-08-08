import sys
import json

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
    print('Please download the required modules from requirements.txt')
    sys.exit()
    
UA = UserAgent()
SESSION = HTMLSession()

@click.command()
@click.option('--tag', prompt='Please enter a valid sub-reddit tag name!', help='Enter sub-reddit tag name!')
def main(tag):
    """Store last 10 posts for the tags subreddit"""
    click.echo('starting the script!')
    global UA 
    global SESSION
    try:
        divs = get_tag_data(tag, SESSION)
        links = find_posts_links(divs)
        posts = get_posts_data(links, SESSION, UA)
        data = []
        for post in posts:
            data.append(post)

        with open(f"{tag_name}.json", "w", encoding="utf-8") as file_name:
            json.dumps(data, file_name)  
            
    except KeyboardInterrupt:
        print('Exiting!')
        sys.exit()




if __name__ == "__main__":
    main()
