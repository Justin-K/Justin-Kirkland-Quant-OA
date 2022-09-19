from datetime import datetime
from typing import List
from praw import Reddit
from praw.models import Subreddit, Submission
from prawcore.exceptions import PrawcoreException
from errors import SubredditInaccessibleError
from pmaw import PushshiftAPI


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
        for x in cache:
            print(datetime.utcfromtimestamp(x.created_utc))
        print("*********END CACHE DUMP**************")

    def scrape_subreddit(self,
                         subreddit_name: str,
                         start_date: datetime,
                         end_date: datetime,
                         limit=5):
        subreddit = self.validate_subreddit(subreddit_name)
        _pmaw = PushshiftAPI(praw=self.client)
        search = _pmaw.search_submissions(after=int(start_date.timestamp()),
                                         before=int(end_date.timestamp()),
                                         limit=None,
                                         subreddit=subreddit,
                                         filter_fn=lambda t: t["score"] > 0
                                         )

        s_search = sorted([post for post in search], key=lambda x: x["score"], reverse=True)
        return s_search[:limit]


        #for i in search:
            #print(datetime.utcfromtimestamp(i.created_utc))
