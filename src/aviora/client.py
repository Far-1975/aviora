from __future__ import annotations

from typing import Literal, Optional

from .exceptions import AvioraAuthError, AvioraError, AvioraRateLimitError
from .search import SearchClient
from .types import ExtractResult, SearchResult


class Aviora:
    """AI Search Framework powered by Tavily.

    Args:
        api_key: Your Tavily API key. Get one at https://tavily.com
    """

    def __init__(self, api_key: str):
        self._search = SearchClient(api_key=api_key)

    # ------------------------------------------------------------------ #
    # Sync API                                                             #
    # ------------------------------------------------------------------ #

    def search(
        self,
        query: str,
        max_results: int = 5,
        search_depth: Literal["basic", "advanced"] = "advanced",
        topic: Literal["general", "news"] = "general",
        include_domains: Optional[list[str]] = None,
        exclude_domains: Optional[list[str]] = None,
        include_answer: bool = False,
        include_raw_content: bool = False,
    ) -> list[SearchResult]:
        """Search the web and return a ranked list of results.

        Args:
            query: The search query.
            max_results: Maximum number of results to return (default 5).
            search_depth: ``"basic"`` is faster; ``"advanced"`` is more thorough.
            topic: ``"general"`` for all content; ``"news"`` for recent news.
            include_domains: Only include results from these domains.
            exclude_domains: Exclude results from these domains.
            include_answer: Include a short AI-generated answer in results.
            include_raw_content: Include raw HTML content in results.

        Returns:
            A list of :class:`SearchResult` dicts ordered by relevance score.
        """
        return self._search.search(
            query=query,
            max_results=max_results,
            search_depth=search_depth,
            topic=topic,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            include_answer=include_answer,
            include_raw_content=include_raw_content,
        )

    def qna_search(self, query: str) -> str:
        """Search the web and return a direct answer string.

        Best for questions that have a single factual answer.

        Args:
            query: The question to answer.

        Returns:
            A concise answer string.
        """
        return self._search.qna_search(query=query)

    def get_search_context(self, query: str, max_tokens: int = 4000) -> str:
        """Return a condensed string of web content suitable for RAG pipelines.

        Args:
            query: The search query.
            max_tokens: Approximate token budget for the returned context.

        Returns:
            A single string of relevant web content.
        """
        return self._search.get_search_context(query=query, max_tokens=max_tokens)

    def extract(self, urls: list[str]) -> list[ExtractResult]:
        """Extract clean content from one or more URLs.

        Args:
            urls: List of URLs to extract content from.

        Returns:
            A list of :class:`ExtractResult` dicts.
        """
        return self._search.extract(urls=urls)

    def crawl(
        self,
        url: str,
        max_depth: int = 1,
        max_breadth: int = 10,
        limit: int = 20,
    ) -> list[dict]:
        """Crawl a website and return page content.

        Args:
            url: The starting URL to crawl from.
            max_depth: How many link-levels deep to follow.
            max_breadth: Max links to follow per page.
            limit: Total page cap.

        Returns:
            A list of crawled page dicts.
        """
        return self._search.crawl(
            url=url, max_depth=max_depth, max_breadth=max_breadth, limit=limit
        )

    def map(self, url: str) -> list[str]:
        """Return all URLs discovered on a website.

        Args:
            url: Root URL to map.

        Returns:
            A list of discovered URLs.
        """
        return self._search.map(url=url)

    # ------------------------------------------------------------------ #
    # Async API                                                            #
    # ------------------------------------------------------------------ #

    async def async_search(
        self,
        query: str,
        max_results: int = 5,
        search_depth: Literal["basic", "advanced"] = "advanced",
        topic: Literal["general", "news"] = "general",
        include_domains: Optional[list[str]] = None,
        exclude_domains: Optional[list[str]] = None,
        include_answer: bool = False,
        include_raw_content: bool = False,
    ) -> list[SearchResult]:
        """Async version of :meth:`search`."""
        return await self._search.async_search(
            query=query,
            max_results=max_results,
            search_depth=search_depth,
            topic=topic,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            include_answer=include_answer,
            include_raw_content=include_raw_content,
        )

    async def async_qna_search(self, query: str) -> str:
        """Async version of :meth:`qna_search`."""
        return await self._search.async_qna_search(query=query)

    async def async_get_search_context(self, query: str, max_tokens: int = 4000) -> str:
        """Async version of :meth:`get_search_context`."""
        return await self._search.async_get_search_context(
            query=query, max_tokens=max_tokens
        )

    async def async_extract(self, urls: list[str]) -> list[ExtractResult]:
        """Async version of :meth:`extract`."""
        return await self._search.async_extract(urls=urls)

