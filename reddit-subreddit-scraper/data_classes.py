import datetime
from typing import List
from dataclasses import dataclass


@dataclass
class RedditUser:
    user_name: str
    created_on: str
    id: str
    comment_karma: int
    has_reddit_gold: bool


@dataclass
class Base:
    author: RedditUser
    id: str
    upvotes: int
    created_on: str


@dataclass
class RedditPostComment(Base):
    text_html: str


@dataclass
class RedditPost(Base):
    comments: List[RedditPostComment]
    title: str


@dataclass
class SubredditData:
    num_accounts_less_than_three_months_old: int
    top_posts_and_comments: List[RedditPost]