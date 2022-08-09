# Reddit-Posts-Scraper

Python Reddit scraper is built on pure web-scraping(no API used), the code works on any valid sub-reddit tag name.

---

## Format
* Json

## Output
Most Recent 10 to 20 posts depending on user input.
All JSON files are stored in /data.
if data is not present: its the value will be null. 

## JSON fields
* Author
* Author link
* raw timestamp
* Posted on
* Title
* Description
* Post link
  * embedded links
  * external links


## Set Up
1. In the Reddit-Scraper root directory, clone the project using 
```
git clone https://github.com/huzai786/Reddit-Scrapper.git
```

2. Set up a virtual environment
```
python -m venv venv
```

3. Activate the virtual environment
- Windows: `env\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Install required packages
```
pip install -r requirements.txt
```

## Usage
```
$ py main.py --help
Usage: main.py [OPTIONS]

  Scrape last 10-20 posts for the given subreddit

Options:
  --tag TEXT    Valid sub-reddit tag name. for example [python, webdev,
                announcements, funny]
  --tp INTEGER  Total number of posts to scrape, 10-20.  [default: 10] 
  --help        Show this message and exit.
  ```
To run:
```
python main.py --tag [Tag name] --tp [Total Posts]
```
