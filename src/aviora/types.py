from typing import Optional
from typing_extensions import TypedDict


class SearchResult(TypedDict):
    title: str
    url: str
    content: str
    score: float
    raw_content: Optional[str]


class ExtractResult(TypedDict):
    url: str
    raw_content: str
    images: list[str]
