import datetime
from typing import List
from praw import Reddit
from praw.models import Subreddit, Submission
from prawcore.exceptions import PrawcoreException
from errors import SubredditInaccessibleError
from enums import Timeframe
from data_classes import SubredditResult, Post


class SubredditScraper:
    MAX_CACHE: int = 50

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

    def __process_cache(self, cache: List[Submission]):
        pass

    def scrape_subreddit(self,
                         subreddit_name: str,
                         timeframe: Timeframe = Timeframe.ALL,
                         timeframe_scalar: int = 1,
                         ):
        subreddit = self.validate_subreddit(subreddit_name)
        if timeframe == Timeframe.YEAR and timeframe_scalar > 1:
            timeframe = Timeframe.ALL
        if timeframe is not Timeframe.ALL:
            start: int = int((datetime.datetime.utcnow() - datetime.timedelta(
                milliseconds=timeframe.value * timeframe_scalar
                )).timestamp())
        else:
            start: int = int(datetime.datetime(1970, 1, 1).timestamp())
        cache: List[Submission] = []

        for post in subreddit.top(time_filter=timeframe.name.lower()):
            if post.created_utc > start:
                if len(cache) >= SubredditScraper.MAX_CACHE:
                    self.__process_cache(cache)
                    cache.clear()
                else:
                    cache.append(post)
        if cache:
            self.__process_cache(cache)
            cache.clear()


