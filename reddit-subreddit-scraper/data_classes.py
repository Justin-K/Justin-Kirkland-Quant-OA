from typing import List
from dataclasses import dataclass


@dataclass
class RedditUser:
    """
        Represents a Reddit user.

            Attributes
            ----------
            user_name : str
                Username of the Reddit user
            created_on : str
                A string representing the date (UTC) when the user created their account.
            user_id : str
                A base-32 Reddit user id used to identify the user.
            comment_karma : int
                Represents how much comment karma the user has.
            has_reddit_gold : bool
                Does the user have active Reddit Premium?

            Methods
            -------
            to_dict() -> dict:
                Returns a dictionary representation of the object to facilitate serialization.
    """
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
    """
    Represents a comment made on a subreddit post.

            Attributes
            ----------
            author : str
                The username of the user who wrote the comment.
            id : str
                The base-32 Reddit id of the comment.
            upvotes : int
                The amount of upvotes the comment has.
            created_on : str
                A string representing the date (UTC) when the comment was written.
            text_html : str
                The body of the comment in HTML.

            Methods
            -------
            to_dict() -> dict:
                Returns a dictionary representation of the object to facilitate serialization.
    """
    text_html: str

    def to_dict(self):
        x = super().to_dict().copy()
        x["text_html"] = self.text_html
        return x


@dataclass
class RedditPost(Base):
    """
    Represents a post on a subreddit.

            Attributes
            ----------
            author : str
                The username of the user who wrote the comment.
            id : str
                The base-32 Reddit id of the comment.
            upvotes : int
                The amount of upvotes the comment has.
            created_on : str
                A string representing the date (UTC) when the comment was written.
            post_comments : List[RedditPostComment]
                A list of comments made on the post.
            post_title: str
                The title of the post.

            Methods
            -------
            to_dict() -> dict:
                Returns a dictionary representation of the object to facilitate serialization.
    """
    post_comments: List[RedditPostComment]
    post_title: str

    def to_dict(self):
        x = super().to_dict().copy()
        x["post_comments"] = [i.to_dict() for i in self.post_comments]
        x["post_title"] = self.post_title
        return x


@dataclass
class SubredditData:
    """
    Represents the 5 top subreddit posts and the 6 top comments made to each post.

            Attributes
            ----------
            num_accounts_less_than_three_months_old : int
                The number of accounts that are younger than three months old
            top_posts_and_comments : List[RedditPost]
                A list of the top 5 posts and the top 6 comments on each post.

            Methods
            -------
            to_dict() -> dict:
                Returns a dictionary representation of the object to facilitate serialization.
    """
    num_accounts_less_than_three_months_old: int
    top_posts_and_comments: List[RedditPost]

    def to_dict(self):
        return {
            "new_accounts_less_than_3m_old": f"{self.num_accounts_less_than_three_months_old}",
            "top_posts_and_comments": [i.to_dict() for i in self.top_posts_and_comments]
        }
