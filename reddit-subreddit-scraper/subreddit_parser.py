from typing import List
from praw.models import Submission
from data_classes import SubredditData, RedditPostComment, RedditPost, RedditUser
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from errors import DataIsNoneError
from json import dumps, load


class SubredditProcessor:
    """
    A class to process and parse the data scraped by scraper.SubredditScraper into the dataclasses in data_classes.py
    """
    def __init__(self, submissions: List[Submission], num_new_accounts: int):
        self.__content = submissions
        self.__parsed_submissions: List[RedditPost] = []
        self.__num_new_accounts = num_new_accounts

    def __parse(self, submission: Submission) -> None:
        comments = submission.comments.list()[:6]
        parsed_comments: List[RedditPostComment] = []
        for c in comments:
            comment_creation_time = str(datetime.utcfromtimestamp(c.created_utc))
            comment_op = RedditUser(
                user_name=c.author.name,
                created_on=c.author.created_utc,
                user_id=c.author.id,
                comment_karma=c.author.comment_karma,
                has_reddit_gold=c.author.is_gold,
            )
            post_comment = RedditPostComment(
                author=comment_op,
                id=c.id,
                upvotes=c.score,
                created_on=comment_creation_time,
                text_html=c.body_html
            )
            parsed_comments.append(post_comment)
        post_creation_time = str(datetime.utcfromtimestamp(submission.created_utc))
        submission_op = RedditUser(
            user_name=submission.author.name,
            created_on=submission.author.created_utc,
            user_id=submission.author.id,
            comment_karma=submission.author.comment_karma,
            has_reddit_gold=submission.author.is_gold,
        )

        reddit_post = RedditPost(
            author=submission_op,
            id=submission.id,
            upvotes=submission.score,
            created_on=post_creation_time,
            post_comments=parsed_comments,
            post_title=submission.title
        )
        self.__parsed_submissions.append(reddit_post)

    def __parse_submissions(self) -> None:
        with ThreadPoolExecutor() as exe:
            exe.map(self.__parse, self.__content)

    @property
    def parsed_subreddit_data(self) -> SubredditData:
        self.__parse_submissions()
        subreddit = SubredditData(
            num_accounts_less_than_three_months_old=self.__num_new_accounts,
            top_posts_and_comments=self.__parsed_submissions
        )
        return subreddit


class SubredditJSONSerializer:
    """
        A class to write and load all parsed and processed data by SubredditProcessor to a JSON file.
    """
    def __init__(self, subreddit_obj: SubredditData, file="subreddit_data.json"):
        if not subreddit_obj or not subreddit_obj.top_posts_and_comments:
            raise DataIsNoneError("The SubredditData object passed does not contain the necessary data."
                                  "(data_classes.SubredditData.top_posts_and_comments is None)")
        self.subreddit_obj = subreddit_obj
        self.file = file

    def write_as_json(self):
        with open(self.file, "w") as f:
            f.write(dumps(self.subreddit_obj.to_dict(), indent=4))

    def load_as_json(self):
        with open(self.file, "r") as f:
            if len(f.readlines()) != 0:
                f.seek(0)
                json_obj = load(f)
                return json_obj
