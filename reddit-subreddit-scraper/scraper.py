import datetime

from praw import Reddit
from praw.models import Subreddit
from prawcore.exceptions import PrawcoreException
from errors import SubredditInaccessibleError
from enums import Timeframe
from data_classes import SubredditResult
#from datetime import datetime

class SubredditScraper:

    def __init__(self, site: str):
        self.client = Reddit(
            site,
            user_agent="script:quant_oa_bot:v1 (by u/Anon_4306)"
        )

    def validate_subreddit(self, subreddit_name: str) -> Subreddit:
        if subreddit_name[0: 2] == "r/" or subreddit_name[0: 2] == "R/":
            subreddit_name = subreddit_name[2: len(subreddit_name)]
        try:
            sreddit = self.client.subreddit(subreddit_name)
            type_: str = sreddit.subreddit_type
            if type_ != "public":
                raise SubredditInaccessibleError(f"The subreddit \"r/{subreddit_name}\" is not public.")
        except PrawcoreException as e:
            raise SubredditInaccessibleError(f"The subreddit \"r/{subreddit_name}\" is inaccessible.") from e
        return sreddit

    def scrape_subreddit(self,
                         subreddit_name: str,
                         timeframe: Timeframe = Timeframe.WEEK,
                         limit: int = 5):
        subreddit = self.validate_subreddit(subreddit_name)
        result: SubredditResult = SubredditResult()
        for post in subreddit.top(time_filter=timeframe.value, limit=10):
            pass
            # print(datetime.datetime.utcfromtimestamp(post.created_utc), post.id)
            # for comment in post.comments:
            #     pass
