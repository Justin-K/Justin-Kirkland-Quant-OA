from typing import List, Dict
from praw.models import Redditor
from datetime import date


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
        self.is_image: bool = False


class SubredditResult:

    def __init__(self) -> None:
        self.accounts: int = 0
        self.top_posts: Dict[date: Post] = {}
