"""Tests for Aviora — uses mocking so no real API key is needed."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aviora import Aviora, AvioraAuthError, AvioraRateLimitError, AvioraError


FAKE_RESULTS = [
    {"title": "Test", "url": "https://example.com", "content": "Test content", "score": 0.9, "raw_content": None}
]


@pytest.fixture
def client():
    with patch("aviora.search.TavilyClient"), patch("aviora.search.AsyncTavilyClient"):
        return Aviora(api_key="tvly-test")


# ------------------------------------------------------------------ #
# search()                                                             #
# ------------------------------------------------------------------ #

class TestSearch:
    def test_returns_results(self, client):
        client._search.client.search.return_value = {"results": FAKE_RESULTS}
        results = client.search("AI news")
        assert results == FAKE_RESULTS

    def test_passes_max_results(self, client):
        client._search.client.search.return_value = {"results": FAKE_RESULTS}
        client.search("AI news", max_results=3)
        call_kwargs = client._search.client.search.call_args.kwargs
        assert call_kwargs["max_results"] == 3

    def test_passes_topic(self, client):
        client._search.client.search.return_value = {"results": FAKE_RESULTS}
        client.search("AI news", topic="news")
        call_kwargs = client._search.client.search.call_args.kwargs
        assert call_kwargs["topic"] == "news"

    def test_passes_include_domains(self, client):
        client._search.client.search.return_value = {"results": FAKE_RESULTS}
        client.search("AI news", include_domains=["bbc.com"])
        call_kwargs = client._search.client.search.call_args.kwargs
        assert "bbc.com" in call_kwargs["include_domains"]


# ------------------------------------------------------------------ #
# qna_search()                                                         #
# ------------------------------------------------------------------ #

class TestQnaSearch:
    def test_returns_string(self, client):
        client._search.client.qna_search.return_value = "Sam Altman"
        answer = client.qna_search("Who runs OpenAI?")
        assert answer == "Sam Altman"


# ------------------------------------------------------------------ #
# get_search_context()                                                 #
# ------------------------------------------------------------------ #

class TestGetSearchContext:
    def test_returns_string(self, client):
        client._search.client.get_search_context.return_value = "Some context text"
        ctx = client.get_search_context("RAG pipelines")
        assert isinstance(ctx, str)
        assert ctx == "Some context text"

    def test_passes_max_tokens(self, client):
        client._search.client.get_search_context.return_value = "ctx"
        client.get_search_context("query", max_tokens=1000)
        call_kwargs = client._search.client.get_search_context.call_args.kwargs
        assert call_kwargs["max_tokens"] == 1000


# ------------------------------------------------------------------ #
# extract()                                                            #
# ------------------------------------------------------------------ #

class TestExtract:
    def test_returns_results(self, client):
        extract_results = [{"url": "https://example.com", "raw_content": "Hello", "images": []}]
        client._search.client.extract.return_value = {"results": extract_results}
        out = client.extract(["https://example.com"])
        assert out == extract_results


# ------------------------------------------------------------------ #
# Error handling                                                       #
# ------------------------------------------------------------------ #

class TestErrorHandling:
    def test_auth_error(self, client):
        client._search.client.search.side_effect = Exception("Unauthorized: invalid api key")
        with pytest.raises(AvioraAuthError):
            client.search("test")

    def test_rate_limit_error(self, client):
        client._search.client.search.side_effect = Exception("429 rate limit exceeded")
        with pytest.raises(AvioraRateLimitError):
            client.search("test")

    def test_generic_error(self, client):
        client._search.client.search.side_effect = Exception("Something went wrong")
        with pytest.raises(AvioraError):
            client.search("test")


# ------------------------------------------------------------------ #
# Async methods                                                        #
# ------------------------------------------------------------------ #

class TestAsyncSearch:
    @pytest.mark.asyncio
    async def test_async_search_returns_results(self, client):
        client._search.async_client.search = AsyncMock(
            return_value={"results": FAKE_RESULTS}
        )
        results = await client.async_search("AI news")
        assert results == FAKE_RESULTS

    @pytest.mark.asyncio
    async def test_async_qna_search(self, client):
        client._search.async_client.qna_search = AsyncMock(return_value="42")
        answer = await client.async_qna_search("What is the answer?")
        assert answer == "42"

    @pytest.mark.asyncio
    async def test_async_get_search_context(self, client):
        client._search.async_client.get_search_context = AsyncMock(return_value="context")
        ctx = await client.async_get_search_context("LLMs")
        assert ctx == "context"

    @pytest.mark.asyncio
    async def test_async_extract(self, client):
        extract_results = [{"url": "https://example.com", "raw_content": "Hi", "images": []}]
        client._search.async_client.extract = AsyncMock(
            return_value={"results": extract_results}
        )
        out = await client.async_extract(["https://example.com"])
        assert out == extract_results
