from __future__ import annotations

from typing import Literal, Optional

from tavily import AsyncTavilyClient, TavilyClient

from .exceptions import AvioraAuthError, AvioraRateLimitError, AvioraError
from .types import ExtractResult, SearchResult


class SearchClient:

    def __init__(self, api_key: str):
        self._api_key = api_key
        self.client = TavilyClient(api_key=api_key)
        self.async_client = AsyncTavilyClient(api_key=api_key)

    def _handle_error(self, exc: Exception) -> None:
        msg = str(exc).lower()
        if "unauthorized" in msg or "invalid api key" in msg or "401" in msg:
            raise AvioraAuthError("Invalid API key. Get one at https://tavily.com") from exc
        if "rate limit" in msg or "429" in msg:
            raise AvioraRateLimitError("Rate limit exceeded. Upgrade your Tavily plan.") from exc
        raise AvioraError(str(exc)) from exc

    # ------------------------------------------------------------------ #
    # Sync methods                                                         #
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
        try:
            response = self.client.search(
                query=query,
                search_depth=search_depth,
                topic=topic,
                max_results=max_results,
                include_domains=include_domains or [],
                exclude_domains=exclude_domains or [],
                include_answer=include_answer,
                include_raw_content=include_raw_content,
            )
            return response["results"]
        except Exception as exc:
            self._handle_error(exc)

    def qna_search(self, query: str) -> str:
        try:
            return self.client.qna_search(query=query)
        except Exception as exc:
            self._handle_error(exc)

    def get_search_context(self, query: str, max_tokens: int = 4000) -> str:
        try:
            return self.client.get_search_context(query=query, max_tokens=max_tokens)
        except Exception as exc:
            self._handle_error(exc)

    def extract(self, urls: list[str]) -> list[ExtractResult]:
        try:
            response = self.client.extract(urls=urls)
            return response.get("results", [])
        except Exception as exc:
            self._handle_error(exc)

    def crawl(
        self,
        url: str,
        max_depth: int = 1,
        max_breadth: int = 10,
        limit: int = 20,
    ) -> list[dict]:
        try:
            response = self.client.crawl(
                url=url,
                max_depth=max_depth,
                max_breadth=max_breadth,
                limit=limit,
            )
            return response.get("results", [])
        except Exception as exc:
            self._handle_error(exc)

    def map(self, url: str) -> list[str]:
        try:
            response = self.client.map(url=url)
            return response.get("urls", [])
        except Exception as exc:
            self._handle_error(exc)

    # ------------------------------------------------------------------ #
    # Async methods                                                        #
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
        try:
            response = await self.async_client.search(
                query=query,
                search_depth=search_depth,
                topic=topic,
                max_results=max_results,
                include_domains=include_domains or [],
                exclude_domains=exclude_domains or [],
                include_answer=include_answer,
                include_raw_content=include_raw_content,
            )
            return response["results"]
        except Exception as exc:
            self._handle_error(exc)

    async def async_qna_search(self, query: str) -> str:
        try:
            return await self.async_client.qna_search(query=query)
        except Exception as exc:
            self._handle_error(exc)

    async def async_get_search_context(self, query: str, max_tokens: int = 4000) -> str:
        try:
            return await self.async_client.get_search_context(
                query=query, max_tokens=max_tokens
            )
        except Exception as exc:
            self._handle_error(exc)

    async def async_extract(self, urls: list[str]) -> list[ExtractResult]:
        try:
            response = await self.async_client.extract(urls=urls)
            return response.get("results", [])
        except Exception as exc:
            self._handle_error(exc)

