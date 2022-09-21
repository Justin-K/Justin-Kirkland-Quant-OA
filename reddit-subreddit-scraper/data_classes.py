import datetime
from typing import List
from dataclasses import dataclass

@dataclass
class RedditUser:
    user_name: str
    created_on: str
    user_id: str
    comment_karma: int
    has_reddit_gold: bool

    def to_dict(self):
        return {
            "user_name": self.user_name,
            "created_on": self.created_on,
            "user_id": self.user_id,
            "comment_karma": self.comment_karma,
            "has_reddit_gold": self.has_reddit_gold
        }


@dataclass
class Base:
    author: RedditUser
    id: str
    upvotes: int
    created_on: str

    def to_dict(self):
        return {
            "author": self.author.to_dict(),
            "id": self.id,
            "upvotes": self.upvotes,
            "created_on": self.created_on
        }

@dataclass
class RedditPostComment(Base):
    text_html: str

    def to_dict(self):
        x = super().to_dict().copy()
        x["text_html"] = self.text_html
        return x


@dataclass
class RedditPost(Base):
    post_comments: List[RedditPostComment]
    post_title: str

    def to_dict(self):
        x = super().to_dict().copy()
        x["post_comments"] = [i.to_dict() for i in self.post_comments]
        x["post_title"] = self.post_title
        return x


@dataclass
class SubredditData:
    num_accounts_less_than_three_months_old: int
    top_posts_and_comments: List[RedditPost]

    def to_dict(self):
        return {
            "new_accounts_less_than_3m_old" : f"{self.num_accounts_less_than_three_months_old}",
            "top_posts_and_comments": [i.to_dict() for i in self.top_posts_and_comments]
        }