# Aviora

<p align="center">
  <b>AI Search Framework powered by Tavily</b><br>
  Build AI agents and RAG pipelines with real-time web search in minutes.
</p>

<p align="center">
  <a href="https://github.com/Far-1975/aviora/actions"><img src="https://github.com/Far-1975/aviora/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/aviora/"><img src="https://img.shields.io/pypi/v/aviora?color=blue&label=PyPI" alt="PyPI"></a>
  <a href="https://pypi.org/project/aviora/"><img src="https://img.shields.io/pypi/dm/aviora?color=brightgreen&label=Downloads" alt="Downloads"></a>
  <a href="https://pypi.org/project/aviora/"><img src="https://img.shields.io/pypi/pyversions/aviora" alt="Python versions"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>
</p>

---

## Why Aviora?

- **Real-time web search** — powered by Tavily's AI-optimized search index
- **Sync & async** — native `async/await` support for every method
- **RAG-ready** — `get_search_context()` returns a clean text blob for LLM context windows
- **Q&A search** — `qna_search()` returns a single direct answer string
- **Extract & crawl** — pull clean content from any URL or entire websites
- **Typed** — full `TypedDict` return types + PEP 561 `py.typed` marker for mypy/pyright
- **Simple error handling** — `AvioraAuthError`, `AvioraRateLimitError`

---

## Installation

```bash
pip install aviora
```

Get a free Tavily API key at [tavily.com](https://tavily.com).

---

## Quick Start

```python
from aviora import Aviora

client = Aviora(api_key="tvly-xxxx")

results = client.search("Latest AI news")

for r in results:
    print(r["title"], r["url"])
```

---

## All Features

### Standard Search

```python
results = client.search(
    "OpenAI GPT-5 release date",
    max_results=10,
    search_depth="advanced",    # "basic" | "advanced"
    topic="general",             # "general" | "news"
    include_domains=["techcrunch.com", "wired.com"],
    exclude_domains=["reddit.com"],
)

for r in results:
    print(r["title"])   # page title
    print(r["url"])     # source URL
    print(r["content"]) # relevant snippet
    print(r["score"])   # relevance score (0–1)
```

### Direct Q&A

Get a single-sentence answer instead of a list of links:

```python
answer = client.qna_search("Who is the CEO of OpenAI?")
print(answer)  # "Sam Altman"
```

### RAG Context

Get a clean text blob ready to drop straight into an LLM prompt:

```python
context = client.get_search_context(
    "Explain transformer attention mechanisms",
    max_tokens=4000,
)

prompt = f"Answer the question using this context:\n\n{context}\n\nQuestion: ..."
```

### Extract Content from URLs

```python
results = client.extract(["https://openai.com/blog/gpt-4"])

for r in results:
    print(r["url"])
    print(r["raw_content"])
```

### Crawl a Website

```python
pages = client.crawl(
    "https://docs.python.org",
    max_depth=2,
    max_breadth=10,
    limit=50,
)
```

### Map a Website

```python
urls = client.map("https://docs.python.org")
print(urls)  # ["https://docs.python.org/3/", ...]
```

---

## Async Support

Every method has an `async_` counterpart, perfect for use inside FastAPI, LangChain agents, or any async framework:

```python
import asyncio
from aviora import Aviora

client = Aviora(api_key="tvly-xxxx")

async def main():
    # Run multiple searches concurrently
    results, answer, context = await asyncio.gather(
        client.async_search("AI news today"),
        client.async_qna_search("What is LangGraph?"),
        client.async_get_search_context("RAG pipeline best practices"),
    )
    print(results)
    print(answer)
    print(context)

asyncio.run(main())
```

---

## Error Handling

```python
from aviora import Aviora, AvioraAuthError, AvioraRateLimitError, AvioraError

client = Aviora(api_key="tvly-xxxx")

try:
    results = client.search("AI news")
except AvioraAuthError:
    print("Invalid API key")
except AvioraRateLimitError:
    print("Rate limit hit — upgrade at tavily.com")
except AvioraError as e:
    print(f"Search failed: {e}")
```

---

## Use with LangChain / LLM Agents

Aviora's `get_search_context` and `qna_search` methods integrate naturally into any LLM agent:

```python
from aviora import Aviora

client = Aviora(api_key="tvly-xxxx")

def search_tool(query: str) -> str:
    """Tool used by an LLM agent to search the web."""
    return client.get_search_context(query, max_tokens=2000)
```

---

## API Reference

| Method | Description |
|---|---|
| `search(query, ...)` | Web search → `list[SearchResult]` |
| `qna_search(query)` | Direct answer → `str` |
| `get_search_context(query, max_tokens)` | RAG context → `str` |
| `extract(urls)` | Extract page content → `list[ExtractResult]` |
| `crawl(url, ...)` | Crawl a site → `list[dict]` |
| `map(url)` | Discover site URLs → `list[str]` |
| `async_search(...)` | Async version of `search` |
| `async_qna_search(...)` | Async version of `qna_search` |
| `async_get_search_context(...)` | Async version of `get_search_context` |
| `async_extract(...)` | Async version of `extract` |

---

## License

MIT © [Syed Faisal](https://github.com/Far-1975)

