import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# TEXT SNAPSHOT (NO AI)
# ---------------------------
def render_snapshot(metrics):
    return f"""
FOCUS DRIFT — SESSION SNAPSHOT

Duration: {metrics['durationSec']} seconds

Tab Switches: {metrics['tabSwitches']}
Rapid Switches: {metrics['rapidSwitches']}
Unique Domains: {metrics['uniqueDomains']}

(Rapid = switching tabs within ~15 seconds)
"""


# ---------------------------
# LLM ANALYSIS
# ---------------------------
SYSTEM_PROMPT = """
You analyze a single browsing session.

Write in a concise, neutral tone.
No motivation. No advice paragraphs.

Use EXACTLY this format:

• What happened:
- One short sentence describing the main behavior.

• Why it matters:
- One short sentence explaining the effect of this pattern.

• One thing to try:
- One small, practical suggestion.

Rules:
- No more than 3 bullets total
- No fluff
- No assumptions about intent
- No productivity judgment
"""


def analyze_with_llm(metrics):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"""
Session details:
Duration: {metrics['durationSec']} seconds
Tab switches: {metrics['tabSwitches']}
Rapid switches: {metrics['rapidSwitches']}
Switches per minute: {metrics['switchRatePerMin']}
Unique domains: {metrics['uniqueDomains']}
"""
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            "What happened:\n"
            "The session involved frequent switching between different tabs.\n\n"
            "Why this matters:\n"
            "Frequent switching can make it harder to stay focused on one task.\n\n"
            "One thing worth trying:\n"
            "Try staying on one tab for a few minutes before switching."
        )
