import time
from datetime import datetime, timedelta
from typing import List
from praw import Reddit
from praw.models import Subreddit, Submission
from praw.models.comment_forest import CommentForest
from pmaw import Response
from prawcore.exceptions import PrawcoreException
from errors import SubredditInaccessibleError
from pmaw import PushshiftAPI
from concurrent.futures import ThreadPoolExecutor


class SubredditScraper:

    # all api calls return lazy objects; the actual data is only fetched from the api when it is "needed"

    def __init__(self, site: str):
        self.client = Reddit(
            site,
            user_agent="script:quant_oa_bot:v1 (by u/Anon_4306)"
        )
        self.pmaw_client = PushshiftAPI(praw=self.client, num_workers=15, jitter="decorr")

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
                         filter_fn=lambda t: t["score"] > 0, **kwargs) -> Response:
        subreddit = self.validate_subreddit(subreddit_name)

        search = self.pmaw_client.search_submissions(after=int(start_date.timestamp()),
                                                     before=int(end_date.timestamp()),
                                                     subreddit=subreddit,
                                                     filter_fn=filter_fn,
                                                     )
        return search

    def get_top_submissions(self, subreddit: str,
                            start_date: datetime,
                            end_date: datetime,
                            limit=5) -> List[Response]:
        search = self.scrape_subreddit(subreddit,
                                       start_date,
                                       end_date,
                                       )

        search = [i for i in search]
        s_search = sorted(search, key=lambda x: x["score"], reverse=True)
        return s_search[:limit]

    def get_top_submissions_and_comments(self, subreddit, start_date, end_date):
        search = self.get_top_submissions(subreddit,
                                          start_date,
                                          end_date)
        submission_ids = [i["id"] for i in search]
        submissions = [self.client.submission(i) for i in submission_ids]

        def sort_(submission):
            submission.comment_sort = "top"
            submission.comments = submission.comments.list()

        with ThreadPoolExecutor(max_workers=13) as exe:
            exe.map(sort_, submissions)
        return submissions
