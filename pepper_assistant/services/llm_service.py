import os
import random
from typing import Iterable, List, Dict

import requests


# Minimal system instruction per user requirement
SYSTEM_INSTRUCTION = (
    "You are an expert assistant specialized ONLY in hot pepper cultivation. "
    "Give short, practical answers. If the question is outside pepper cultivation, politely refuse and redirect. "
    "Do not provide medical or chemical dosage advice."
)


def _mock_response(user_message: str) -> str:
    """Very small keyword-based mock fallback."""
    if not user_message:
        return "Ask me anything about growing hot peppers."
    text = user_message.lower()
    if any(k in text for k in ['germinat', 'seed', 'germination', 'seedling']):
        return "For germination: keep seeds warm (24–30°C), keep soil moist (not soggy), and provide gentle light after sprouting."
    if 'yellow' in text:
        return "Yellow leaves often indicate overwatering or nutrient issues — check moisture, drainage and light."
    if any(k in text for k in ['aphid', 'pest', 'pests', 'mite']):
        return "Inspect undersides of leaves, wash with water, try insecticidal soap or beneficial insects for small infestations."
    if any(k in text for k in ['water', 'watering']):
        return "Water when the top 2-3 cm of soil are dry; use well-draining soil."
    # fallback generic
    return random.choice([
        "Use well-draining soil and 6-8 hours of light.",
        "Start seeds indoors early and harden off before transplanting.",
    ])


def _build_messages(conversation_messages: Iterable, user_message: str, context_limit: int = 10) -> List[Dict]:
    """Build chat-style messages: system, last N messages, then user message."""
    messages: List[Dict] = []
    # system message first
    messages.append({"role": "system", "content": SYSTEM_INSTRUCTION})

    # add last N messages from conversation_messages (try queryset first)
    try:
        recent = list(conversation_messages.order_by('-created_at')[:context_limit])[::-1]
    except Exception:
        try:
            recent = list(conversation_messages)[-context_limit:]
        except Exception:
            recent = []

    for m in recent:
        role = 'user' if m.role == 'user' else 'assistant'
        messages.append({"role": role, "content": str(m.content)})

    # current user message
    messages.append({"role": "user", "content": user_message})
    return messages


def _call_hf_chat(model: str, api_key: str, messages: List[Dict], max_tokens: int, temperature: float) -> str:
    """Call Hugging Face Inference API using a chat-style messages payload.

    This uses the inference endpoint and sends JSON with `inputs: {"messages": [...]}` when possible.
    Different HF models may return different shapes; handle common patterns and fall back to mock.
    """
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": {"messages": messages},
        "parameters": {"max_new_tokens": max_tokens, "temperature": temperature},
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # handle common response shapes
    # 1) list like [{"generated_text": "..."}]
    if isinstance(data, list) and len(data) > 0:
        first = data[0]
        if isinstance(first, dict):
            if 'generated_text' in first:
                return first['generated_text'].strip()
            # some chat models return 'generated_text' under different keys
            for v in first.values():
                if isinstance(v, str):
                    return v.strip()

    # 2) dict with 'generated_text'
    if isinstance(data, dict):
        if 'generated_text' in data and isinstance(data['generated_text'], str):
            return data['generated_text'].strip()
        # some HF chat models return {'generated_text': '...', 'error': ...}
        # or {'choices': [{'message': {'content': '...'}}]}
        choices = data.get('choices')
        if isinstance(choices, list) and len(choices) > 0:
            first = choices[0]
            if isinstance(first, dict):
                # try message.content
                msg = first.get('message')
                if isinstance(msg, dict) and 'content' in msg:
                    content = msg['content']
                    if isinstance(content, str):
                        return content.strip()
                # try text fields
                for v in first.values():
                    if isinstance(v, str):
                        return v.strip()

    # if we didn't understand response, raise to trigger fallback
    raise RuntimeError('Unexpected HF response format')


def generate_pepper_response(user_message: str, conversation_messages=None, *, max_tokens: int = 300,
                             temperature: float = 0.2, context_limit: int = 10) -> str:
    """Provider switch: 'mock' or 'hf'. Minimal MVP implementation.

    - Build chat-style messages for HF when used.
    - On any error or missing API key, fall back to `_mock_response`.
    """
    provider = os.environ.get('LLM_PROVIDER', 'mock').lower()
    if provider not in ('mock', 'hf'):
        provider = 'mock'

    # Quick guard
    if not user_message:
        return _mock_response(user_message)

    # If provider is mock, return mock immediately
    if provider == 'mock':
        return _mock_response(user_message)

    # provider == 'hf'
    hf_key = os.environ.get('HF_API_KEY')
    if not hf_key:
        return _mock_response(user_message)

    model = os.environ.get('HF_MODEL', 'google/flan-t5-small')

    messages = _build_messages(conversation_messages, user_message, context_limit=context_limit)

    try:
        text = _call_hf_chat(model=model, api_key=hf_key, messages=messages, max_tokens=max_tokens, temperature=temperature)
        if not text or not isinstance(text, str):
            return _mock_response(user_message)
        return text
    except Exception:
        # any error -> fallback to mock
        return _mock_response(user_message)


