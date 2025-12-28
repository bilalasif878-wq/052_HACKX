import os
import json

from openai import OpenAI
from process_session import process_session

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You analyze a single browsing session and point out one clear behavioral pattern.

Write like a calm, observant human.
Not a coach. Not a psychologist. Not an academic.

Rules:
- Use simple, everyday language
- Be concrete and specific (use rates, rough timing, comparisons)
- Do NOT repeat raw stats already shown elsewhere
- Do NOT speculate about motivation, productivity, or intent
- Avoid buzzwords, jargon, and advice-blog tone
- Keep it short and readable

Use EXACTLY this structure:

What happened:
- One concise observation describing the main pattern, using numbers or rates

Why this matters:
- One plain sentence explaining the practical effect of this pattern

One thing worth trying:
- Exactly ONE small, realistic experiment the user could try next time
"""

def build_user_prompt(metrics):
    return f"""
Session facts:

Duration: {metrics['durationSec']} seconds
Tab switches: {metrics['tabSwitches']}
Rapid switches: {metrics['rapidSwitches']}
Switches per minute: {metrics['switchRatePerMin']}
Unique domains: {metrics['uniqueDomains']}
"""

def bar(value, max_value):
    if max_value == 0:
        return "░" * 10
    filled = int((value / max_value) * 10)
    return "█" * filled + "░" * (10 - filled)

def render_snapshot(metrics):
    return f"""
FOCUS DRIFT — SESSION SNAPSHOT

Duration: {metrics['durationSec']} seconds

Tab Switches:    {bar(metrics['tabSwitches'], metrics['tabSwitches'] + 5)} ({metrics['tabSwitches']})
Rapid Switches: {bar(metrics['rapidSwitches'], metrics['rapidSwitches'] + 5)} ({metrics['rapidSwitches']})
Unique Domains: {metrics['uniqueDomains']}

(Rapid = switching tabs within ~15 seconds)
"""

def analyze_with_llm(metrics):
    user_prompt = build_user_prompt(metrics)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SAMPLE_PATH = os.path.join(BASE_DIR, "sample_session.json")

    with open(SAMPLE_PATH, "r") as f:
        session = json.load(f)

    metrics = process_session(session)

    # 1. Visual snapshot
    print(render_snapshot(metrics))

    # 2. Insight
    insight = analyze_with_llm(metrics)

    print("\n=== FOCUS DRIFT — SESSION INSIGHT ===\n")
    print(insight)