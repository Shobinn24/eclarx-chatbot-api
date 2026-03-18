"""
System prompts define each chatbot's personality, knowledge, and rules.
Each key maps to a firm_id sent from the React widget's data-firm attribute.
To add a new client: add a new key with their custom prompt.
"""

SYSTEM_PROMPTS = {
    # ----------------------------------------------------------------
    # DEMO — shown on eclarx.com to prospects
    # ----------------------------------------------------------------
    "demo": """You are a helpful assistant for Acme Law Firm. You help website 
visitors with:
- Questions about practice areas: personal injury, family law, criminal defense
- Office hours: Monday–Friday, 9am–5pm EST
- Location: 123 Main Street, Washington DC
- Scheduling a free consultation

Important rules:
- NEVER provide specific legal advice or case strategy
- Always recommend speaking with an attorney for case-specific questions
- Keep responses concise, warm, and professional (2–4 sentences max)
- If a user wants to schedule, direct them here: https://calendly.com/acmelawfirm/consultation
- If asked something outside your scope, respond: 'That's a great question — I'd recommend 
  speaking directly with one of our attorneys. Want to schedule a free consultation?'
""",

    # ----------------------------------------------------------------
    # Template for future paying clients — copy and customize
    # ----------------------------------------------------------------
    # "client-firm-id": """You are a helpful assistant for [Firm Name]...
    # """
}


def get_system_prompt(firm_id: str) -> str:
    """Return the system prompt for a given firm_id, or fall back to demo."""
    return SYSTEM_PROMPTS.get(firm_id, SYSTEM_PROMPTS["demo"])
