from requests_html import HTMLSession
from bs4 import BeautifulSoup, Tag
import traceback
import time
import sys


def store_data(reddit_tag):
    session = HTMLSession()
    try:
        r = session.get(f'https://www.reddit.com/r/{reddit_tag}/new/')
        print('Rendering...')
        r.html.render(sleep=4, scrolldown=2, wait=3, timeout=30)
        divs = r.html.find('div#AppRouter-main-content')[0]
        file_name = f'{reddit_tag}_data.html'
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(str(divs.html))

        return file_name

    except Exception:
        traceback.print_exc()
        print('Exiting...')
        sys.exit()


def find_div(file_name):
    try:
        with open(file_name, 'a', encoding='utf-8') as f:
            data = f.read()
        soup = BeautifulSoup(data, 'lxml')
        divs = soup.find('div')
        
    except FileNotFoundError:
        print(f'File: {file_name} Not Found!')
        sys.exit()


def get_posts_data(TagObj):
    try:
        for post in posts:
            post.find()
            
            
            
    except AttributeError:
        traceback.print_exc()
   
    
def main():
    print(dir(Tag))
    


if __name__ == '__main__':
    # fname = store_data('webdev')
    main()
