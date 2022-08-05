from main import store_data
from bs4 import BeautifulSoup
import re
import csv
import pprint

with open('data.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')

posts_selector = '#AppRouter-main-content > div > div > div._3ozFtOe6WpJEMUtxDOIvtU > div._31N0dvxfpsO6Ur5AKx4O5d > div._1OVBBWLtHoSPfGCRaPzpTf._3nSp9cdBpqL13CqjdMr2L_._2OVNlZuUd8L9v0yVECZ2iA > div.rpBJOHq2PR60pnwJlUyP0 > div'
divs = soup.select(posts_selector)


def get_post_data(divs):
    data = []
    for div in divs:
        post_author = div.select('div a[data-testid="post_author_link"]')
        posted_on = div.select('span[data-click-id="timestamp"]')
        post_summary = div.select(
            'div > div > a[data-click-id="body"] > div > h3')
        post_detail = div.select('div > div[data-click-id="text"] > div > p')
        if post_author != []:
            post = []
            if post_detail != []:
                if len(post_detail) > 1:
                    description = ''.join(
                        [d.get_text().strip('\n') for d in post_detail])
                description = post_detail[0].get_text().strip()
            else:
                description = 'No description available'
            posted_date = re.sub(r'\s+', ' ', posted_on[0].get_text().strip())
            description = re.sub(r'\s+', ' ', description)
            summary = re.sub(r'\s+', ' ', post_summary[0].get_text())
            post.extend([post_author[0].get_text(),
                        posted_date, summary, description])
            data.append(post)
    return data


posts = get_post_data(divs)

with open('data1.csv', 'w', newline='', encoding='utf-8') as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerows(posts)
