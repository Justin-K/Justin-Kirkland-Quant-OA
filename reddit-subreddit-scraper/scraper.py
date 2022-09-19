from datetime import datetime
from typing import List
from praw import Reddit
from praw.models import Subreddit, Submission
from prawcore.exceptions import PrawcoreException
from errors import SubredditInaccessibleError
from pmaw import PushshiftAPI


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
                         start_date: datetime,
                         end_date: datetime,
                         filter_fn=lambda t: t["score"] > 0) -> List[Submission]:
        subreddit = self.validate_subreddit(subreddit_name)
        pmaw_client = PushshiftAPI(praw=self.client)
        search = pmaw_client.search_submissions(after=int(start_date.timestamp()),
                                                before=int(end_date.timestamp()),
                                                limit=None,
                                                subreddit=subreddit,
                                                filter_fn=filter_fn
                                                )
        return search

    def get_top_submissions(self, subreddit: str,
                            start_date: datetime,
                            end_date: datetime,
                            limit=5) -> List[Submission]:
        search = self.scrape_subreddit(subreddit, start_date, end_date)
        s_search = sorted([post for post in search], key=lambda x: x["score"], reverse=True)
        return s_search[:limit]
