from utils.openai_client import get_client
from googletrans import Translator

_gt = None
def _gt_client():
    global _gt
    if _gt is None:
        _gt = Translator()
    return _gt

def translate_with_llm(text: str, target_lang_name: str) -> str:
    """
    Ask the LLM to translate naturally for kids.
    """
    client = get_client()
    sys = f"Translate the user's English message into natural {target_lang_name}. Keep it kid-friendly and simple."
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": text}
        ],
        temperature=0.3,
        max_tokens=300
    )
    return resp.choices[0].message.content.strip()

def translate_fallback_googletrans(text: str, target_code: str) -> str:
    """
    Fallback translation using googletrans if LLM is unavailable.
    """
    tr = _gt_client()
    return tr.translate(text, dest=target_code).text
