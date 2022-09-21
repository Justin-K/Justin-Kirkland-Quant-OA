from typing import List
from praw.models import Submission
from data_classes import SubredditData, RedditPostComment, RedditPost
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class SubredditProcessor:

    def __init__(self, submissions: List[Submission], num_new_accounts: int):
        self.__content = submissions
        self.__parsed_submissions: List[RedditPost] = []
        self.__num_new_accounts = num_new_accounts

    def __parse(self, submission: Submission) -> None:
        comments = submission.comments.list()[:6]
        parsed_comments: List[RedditPostComment] = []
        for c in comments:
            comment_creation_time = str(datetime.utcfromtimestamp(c.created_utc))
            post_comment = RedditPostComment(
                author=c.author.name,
                id=c.id,
                upvotes=c.score,
                created_on=comment_creation_time,
                text_html=c.body_html
            )
            parsed_comments.append(post_comment)
        post_creation_time = str(datetime.utcfromtimestamp(submission.created_utc))
        reddit_post = RedditPost(
            author=submission.author.name,
            id=submission.id,
            upvotes=submission.score,
            created_on=post_creation_time,
            comments=parsed_comments,
            title=submission.title
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
