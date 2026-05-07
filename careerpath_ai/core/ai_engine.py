"""
core/ai_engine.py - Groq API + OpenRouter fallback with streaming support
"""
import os
import queue
import threading
import hashlib
import json
import requests
from typing import Callable, Generator

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

SYSTEM_PROMPT = """You are PathAI, an expert career guidance counselor specializing in technology and engineering careers. You help students and professionals choose the right career path, create personalized study plans, and navigate the tech industry.

Your expertise covers: Computer Science, AI/ML, Full Stack Development, Data Science, Cybersecurity, ECE, EEE, IT, DevOps, Mobile Development, and all related engineering fields.

When a user seems confused or undecided, ask targeted questions like:
- What subjects do they enjoy?
- Do they prefer building things, analyzing data, or securing systems?
- What's their current education level?
- Do they prefer creative work or analytical work?

Then recommend a specific roadmap with reasoning. Be warm, encouraging, and specific. Always cite whether resources are free or paid. Format responses with clear sections using markdown-like structure (use **bold** for headings, • for bullet points).

Keep responses concise but thorough. Always end with an encouraging note and offer to dive deeper into any specific area."""

# Response cache: keyed by hash of messages
_response_cache: dict[str, str] = {}
_cache_lock = threading.Lock()


def _cache_key(messages: list[dict]) -> str:
    content = json.dumps(messages, sort_keys=True)
    return hashlib.md5(content.encode()).hexdigest()


def _check_cache(messages: list[dict]) -> str | None:
    key = _cache_key(messages)
    with _cache_lock:
        return _response_cache.get(key)


def _store_cache(messages: list[dict], response: str):
    key = _cache_key(messages)
    with _cache_lock:
        _response_cache[key] = response


# ─── GROQ STREAMING ───────────────────────────────────────────────────────────

def stream_groq(messages: list[dict], chunk_callback: Callable[[str], None], done_callback: Callable[[str], None], error_callback: Callable[[str], None]):
    """Stream response from Groq API. Calls chunk_callback for each token, done_callback when complete."""
    def _worker():
        full_response = ""
        try:
            api_key = os.getenv("GROQ_API_KEY", "")
            if not api_key or api_key == "your_groq_api_key_here":
                raise ValueError("GROQ_API_KEY not configured. Please set it in Settings.")

            if not GROQ_AVAILABLE:
                raise ImportError("groq package not installed")

            client = Groq(api_key=api_key)
            all_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=all_messages,
                stream=True,
                max_tokens=1500,
                temperature=0.7
            )

            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    full_response += delta.content
                    chunk_callback(delta.content)

            _store_cache(messages, full_response)
            done_callback(full_response)

        except Exception as e:
            # Try OpenRouter fallback
            try:
                result = _openrouter_request(messages)
                for char in result:
                    full_response += char
                    chunk_callback(char)
                _store_cache(messages, full_response)
                done_callback(full_response)
            except Exception as e2:
                error_callback(f"Both APIs failed.\nGroq: {str(e)}\nOpenRouter: {str(e2)}")

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
    return thread


def _openrouter_request(messages: list[dict]) -> str:
    """Non-streaming OpenRouter API call as fallback."""
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key or api_key == "your_openrouter_api_key_here":
        raise ValueError("OPENROUTER_API_KEY not configured.")

    all_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://careerpath-ai.app",
            "X-Title": "CareerPath AI"
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": all_messages,
            "max_tokens": 1500,
            "temperature": 0.7
        },
        timeout=60
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def test_groq_connection() -> tuple[bool, str]:
    """Test Groq API connection. Returns (success, message)."""
    try:
        api_key = os.getenv("GROQ_API_KEY", "")
        if not api_key or api_key == "your_groq_api_key_here":
            return False, "API key not set"
        if not GROQ_AVAILABLE:
            return False, "groq package not installed"
        client = Groq(api_key=api_key)
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say 'OK' only."}],
            max_tokens=5
        )
        return True, f"Connected! Model: llama-3.3-70b-versatile"
    except Exception as e:
        return False, str(e)


def test_openrouter_connection() -> tuple[bool, str]:
    """Test OpenRouter API connection. Returns (success, message)."""
    try:
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        if not api_key or api_key == "your_openrouter_api_key_here":
            return False, "API key not set"
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "mistralai/mistral-7b-instruct", "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 5},
            timeout=15
        )
        response.raise_for_status()
        return True, "Connected! Model: mistral-7b-instruct"
    except Exception as e:
        return False, str(e)


def stream_response_to_queue(messages: list[dict], result_queue: queue.Queue):
    """
    Stream AI response, putting chunks into a queue.
    Queue items: ("chunk", text) | ("done", full_text) | ("error", msg)
    Checks cache first.
    """
    cached = _check_cache(messages)
    if cached:
        # Simulate streaming from cache
        def _simulate():
            for char in cached:
                result_queue.put(("chunk", char))
            result_queue.put(("done", cached))
        thread = threading.Thread(target=_simulate, daemon=True)
        thread.start()
        return thread

    def on_chunk(text):
        result_queue.put(("chunk", text))

    def on_done(full_text):
        result_queue.put(("done", full_text))

    def on_error(msg):
        result_queue.put(("error", msg))

    return stream_groq(messages, on_chunk, on_done, on_error)
