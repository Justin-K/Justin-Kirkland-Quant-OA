import datetime
from typing import List
from dataclasses import dataclass


@dataclass
class Base:
    author: str
    id: str
    upvotes: int
    created: datetime.datetime


@dataclass
class RedditPostComment(Base):
    text: str
    total_comments: int


@dataclass
class RedditPost(Base):
    comments: List[RedditPostComment]
    title: str
