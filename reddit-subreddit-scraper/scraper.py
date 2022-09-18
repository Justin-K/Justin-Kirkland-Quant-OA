from praw import Reddit
from prawcore.exceptions import PrawcoreException
from errors import SubredditInaccessibleError


class SubredditScraper:

    def __init__(self, site: str):
        self.client = Reddit(
            site,
            user_agent="script:quant_oa_bot:v1 (by u/Anon_4306)"
        )

    def scrape_subreddit(self, subreddit_name: str):
        if subreddit_name[0: 2] == "r/":
            subreddit_name = subreddit_name[2: len(subreddit_name)]
        try:
            subreddit = self.client.subreddit(subreddit_name)
            type_: str = subreddit.subreddit_type
            if type_ != "public":
                raise SubredditInaccessibleError(f"The subreddit \"r/{subreddit_name}\" is not public.")
        except PrawcoreException as e:
            raise SubredditInaccessibleError(f"The subreddit \"r/{subreddit_name}\" is inaccessible.") from e
