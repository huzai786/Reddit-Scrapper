# Reddit-Posts-Scraper
---
Python Reddit scraper is built on pure web-scraping(no API used), the code works on any valid sub-reddit tag name.


---
## Format
Json

## Output
Most Recent 10 posts.
All JSON files are stored in /data

## JSON fields
if data is not present: its the value will be null. 

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
$ py main.py --help
Usage: main.py [OPTIONS]

  Store last 10 posts for the tags subreddit

Options:
  --tag TEXT  Enter sub-reddit tag name!
  --help      Show this message and exit
  
To run:
```
python main.py [Tag name]
```
