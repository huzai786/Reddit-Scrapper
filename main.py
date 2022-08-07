import sys
import json
import time
import argparse
try:
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
    





def main(ua, session, tag):
    try: 
        divs = get_tag_data(tag, session)
        links = find_posts_links(divs)
        posts = get_posts_data(links, session, ua)
        data = []
        for p in posts:
            data.append(p)

        with open(f"{tag}.json", "w", encoding="utf-8") as f:
            json.dumps(data, f)
            
            
    except KeyboardInterrupt:
        print('Exiting!')
        sys.exit()




if __name__ == "__main__":
    ua = UserAgent()
    session = HTMLSession()
    tag = "Python"
    main(ua, session, tag)
