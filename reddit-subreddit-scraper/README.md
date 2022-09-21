# Reddit Subreddit Scraper
This is my submission for the Quant Reddit Subreddit Scraper Online Assessment. It uses two third-party libraries: praw and pmaw.

Installation
============
1. Clone repository into a directory of your choice.
2. Add praw.ini file with your client key, and your client secret key. Create a new site for these credentials.
    1. See [praw.ini documentation](praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html) for more details
   
3.  Preferably, create a new virtual environment, activate it, and run `pip install -r requirements.txt` to install the needed libraries. Alternatively, run the command from your system-wide installation of Python to install the dependencies globally. 

Quickstart
==========
```
(venv) C:\path\to\reddit-subreddit-scraper\> python subreddit_scraper_cli.py r/gaming "2022-3-3" "2022-9-1" -output_file=YOUR_OUTPUT_FILE.json -comments=200
```
###Code Overview
- scraper.py
  - SubredditScraper
      - The job of this class is to scrape the PushShift.io and Reddit APIs to gather the top 5 posts between two dates, the top 6 replies to each post, and the number of accounts that were created less than 3 months ago.
- data_classes.py
  - RedditUser
    - A collection of attributes that represent a Reddit user
  - Base
    - A collection of common attributes
  - RedditPostComment
    - A collection of attributes representing a comment made on a Reddit post
  - RedditPost
    - A collection of attributes representing a post on a subreddit
  - SubredditData
    - A collection of attributes representing the data scraped
- enums.py
  - Timeframe
    - An Enum representing various periods of time in terms of milliseconds.
- subreddit_parser.py
  - SubredditProcessor
    - A class responsible for processing and parsing the input from SubredditScraper into data classes defined in data_classes.py
  - SubredditJSONSerializer
    - A class responsible for serializing the data classes into a JSON file as well as loading it
- subreddit_scraper_cli.py
    - This file provides the CLI interface to scrape data, process/parse it, and serialize it in one lovely command
