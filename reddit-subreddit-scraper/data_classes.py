from typing import List, Dict
from praw.models import Redditor


class BaseData:

    def __init__(self) -> None:
        self.user: Redditor
        self.text: str = ""
        self.upvotes: int = 0
        self.downvotes: int = 0
        self.timestamp: int = 0


class Comment(BaseData):

    def __init__(self) -> None:
        super().__init__()


class Post(BaseData):

    def __init__(self) -> None:
        super().__init__()
        self.top_replies: List[Comment] = []


class SubredditData:

    def __init__(self) -> None:
        self.accounts: int = 0
        self.top_posts: Dict[int: Post] = {}
