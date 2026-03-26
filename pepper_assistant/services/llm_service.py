import random
import textwrap


# System prompt template - used later when integrating a real LLM
SYSTEM_INSTRUCTION = (
    "You are a concise, expert assistant specialized in hot pepper (capsicum) cultivation. "
    "Always answer from the perspective of an experienced pepper grower. Provide clear, practical advice; "
    "include safety cautions when relevant. Do not provide medical or toxic dosing instructions."
)


def _needs_disclaimer(user_text: str) -> bool:
    text = (user_text or '').lower()
    keywords = ['poison', 'ingest', 'ingested', 'medical', 'toxic', 'overdose', 'dose', 'symptom']
    return any(k in text for k in keywords)


def generate_pepper_response(user_message: str, conversation_messages=None, max_tokens: int = 300, context_limit: int = 10) -> str:
    """
    Mock assistant response generator specialized in hot pepper cultivation.
    - Honors a simple system instruction for consistent tone.
    - Adds a safety disclaimer when harmful keywords are detected.
    - Returns a concise reply (simulated token cap).
    """
    user_text = (user_message or '').strip()
    lower = user_text.lower()

    # Build a simple context summary from the last `context_limit` messages if provided.
    context_summary = ''
    try:
        if conversation_messages is not None:
            recent = list(conversation_messages.order_by('-created_at')[:context_limit])[::-1]
            parts = [f"{m.role}: {m.content}" for m in recent]
            context_summary = "\nContext:\n" + "\n".join(parts)
    except Exception:
        # If conversation_messages is a list or other iterable
        try:
            recent = list(conversation_messages)[-context_limit:]
            parts = [f"{m.role}: {m.content}" for m in recent]
            context_summary = "\nContext:\n" + "\n".join(parts)
        except Exception:
            context_summary = ''

    # Safety disclaimer
    disclaimer = ""
    if _needs_disclaimer(user_text):
        disclaimer = (
            "\n\nDisclaimer: I can provide general gardening information but not medical advice. "
            "If this is an emergency or a health concern, please consult a medical professional or poison control."
        )

    # Domain-specific keyword responses
    if any(k in lower for k in ['germinat', 'germination', 'seed', 'seedling', 'start seeds']):
        resp = (
            "For germination: keep seeds warm (24–30°C/75–86°F), maintain consistent moisture "
            "(use a humidity dome or plastic wrap), and be patient — some varieties take longer. "
            "Use a light, well-draining seed mix and provide bottom heat if possible."
        )
    elif any(k in lower for k in ['yellow', 'yellowing', 'yellow leaves']):
        resp = (
            "Yellow leaves often mean overwatering, poor drainage, or nutrient deficiency. "
            "Check soil moisture, ensure proper drainage, provide enough light, and consider a balanced fertilizer."
        )
    elif any(k in lower for k in ['aphid', 'pest', 'pests', 'bugs', 'mite']):
        resp = (
            "Inspect undersides of leaves for aphids or mites. For small infestations, wash plants with water, "
            "use insecticidal soap, or introduce beneficial insects (ladybugs). Avoid strong chemicals on edible plants."
        )
    elif any(k in lower for k in ['water', 'watering', 'wet', 'dry']):
        resp = (
            "Water when the top 2–3 cm (1 inch) of soil are dry. Use well-draining soil; overwatering causes root problems. "
            "In containers, water more frequently during hot weather."
        )
    elif any(k in lower for k in ['light', 'sun', 'lighting', 'grow light']):
        resp = (
            "Peppers like bright light; aim for 6–8 hours of direct sun outdoors, or provide strong grow lights indoors. "
            "Rotate plants to keep them even."
        )
    else:
        generic = [
            "Make sure soil is well-draining and rich in organic matter; peppers prefer slightly acidic to neutral pH.",
            "Start with good-quality seedlings or start seeds indoors early in the season for a longer growing period.",
            "Monitor plants weekly for pests and signs of nutrient deficiency; apply a balanced fertilizer when needed.",
            "Transplant outside only after the last frost and when soil has warmed. Harden off seedlings gradually."
        ]
        resp = random.choice(generic)

    # Simulate token cap by truncating to approx max_tokens * avg_chars_per_token
    avg_chars_per_token = 4
    max_chars = max_tokens * avg_chars_per_token
    text = (SYSTEM_INSTRUCTION + "\n\n" + resp + disclaimer + context_summary)
    return textwrap.shorten(text, width=max_chars, placeholder='...')

