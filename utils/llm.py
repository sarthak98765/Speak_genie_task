from utils.openai_client import get_client
import config

def kid_safe_reply(user_text: str, roleplay_context: str | None = None) -> str:
    """
    Generate a short, child-friendly tutor response. Adds gentle correction and 1 speaking tip when needed.
    """
    client = get_client()
    sys = config.TUTOR_SYSTEM_PROMPT
    if roleplay_context:
        sys += f"\nContext: The student is practicing a roleplay about: {roleplay_context}."
        sys += "\nStay in character for the scenario while being supportive."

    messages = [
        {"role": "system", "content": sys},
        {"role": "user", "content": user_text.strip()[:4000]}
    ]

    resp = client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=messages,
        temperature=0.6,
        max_tokens=220
    )
    return resp.choices[0].message.content.strip()
