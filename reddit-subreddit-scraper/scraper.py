from typing import List
from datetime import datetime
from praw import Reddit
from praw.models import Submission, Subreddit
from pmaw import Response
from prawcore.exceptions import PrawcoreException
from errors import SubredditInaccessibleError, DateError
from pmaw import PushshiftAPI
from concurrent.futures import ThreadPoolExecutor
from enums import Timeframe
from heapq import nlargest


class SubredditScraper:

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
                         filter_fn=lambda t: t["score"] > 0) -> Response:
        after = int(start_date.timestamp())
        before = int(end_date.timestamp())
        if after < before:
            raise DateError("end_date cannot be before start_date!")
        subreddit = self.validate_subreddit(subreddit_name)
        search = self.pmaw_client.search_submissions(after=after,
                                                     before=before,
                                                     subreddit=subreddit,
                                                     filter_fn=filter_fn,
                                                     )
        return search

    def get_top_submissions(self, subreddit: str,
                            start_date: datetime,
                            end_date: datetime) -> List[Response]:
        search = self.scrape_subreddit(subreddit, start_date, end_date)
        search = [i for i in search]
        s_search = nlargest(5, search, key=lambda x: x["score"])
        return s_search

    def get_top_submissions_and_comments(self, subreddit, start_date, end_date) -> List[Submission]:
        search = self.get_top_submissions(subreddit,
                                          start_date,
                                          end_date)
        submission_ids = [i["id"] for i in search]
        submissions = [self.client.submission(i) for i in submission_ids]

        def sort_(submission):
            submission.comment_sort = "top"
            submission.post_comments = submission.post_comments.list()
        with ThreadPoolExecutor(max_workers=13) as exe:
            exe.map(sort_, submissions)

        return submissions

    '''
        Author: justcool393 @ StackOverflow
        Date: 21 September 2022
        Title: Get Reddit Usernames of Users Who Use a Specific Subreddit
        Type: Source code
        Location: www.stackoverflow.com/a/56452963
        Description: The code snippet "for c in sreddit...created_on.add..." was inspired
        by justcool393's answer to Hillcow's question.
    '''
    def num_new_accounts(self, subreddit, comments_to_scan=200):
        sreddit = self.validate_subreddit(subreddit)
        created_on = set()
        for c in sreddit.comments(limit=comments_to_scan):
            a = c.author
            created_on.add(a.created_utc)
        three_months = Timeframe.MONTH.value * 3
        three_months_timestamp = datetime.now().timestamp() - three_months
        return len([i for i in created_on if i >= three_months_timestamp])
