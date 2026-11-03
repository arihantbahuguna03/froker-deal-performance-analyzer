"""
Creator Deal Performance Analyzer
==================================
Weekly Airflow job that reads post metrics for each completed creator–business
deal and uses Claude 3.5 Sonnet to write a plain-English performance report
for the business owner.

Built Aug 2024 – Aug 2025 using raw Anthropic SDK + Airflow.
No LLM orchestration frameworks — direct API calls only.

Problem:
  A creator posts for a local business. The business owner has no idea
  if it worked. They get a link to an Instagram post, nothing else.
  Without a clear ROI story, businesses don't renew — and the platform
  loses its commission revenue.

Solution:
  Claude reads the raw metrics for each deal and writes a 150-word
  plain-English summary: what reached whom, what actions people took,
  estimated footfall impact, and whether to run the campaign again.
  Delivered to the business owner automatically every Monday morning.
"""

import os
from datetime import datetime

import anthropic
import requests

from demo_data import DEMO_DEALS, SLACK_WEBHOOK_URL


# ── Derived metrics ───────────────────────────────────────────────────────────

def _load_footfall_multipliers() -> tuple[float, float]:
    """
    Load footfall estimation multipliers from analytics_config.py.

    Multipliers estimate real-world store visits from digital engagement
    signals (saves + link clicks). Calibrated against foot-traffic data from
    partner businesses using store counters and QR code redemptions.

    Implementation: proprietary — available on request.
    Copy analytics_config.example.py → analytics_config.py to run with your own values.
    """
    try:
        import analytics_config
        return analytics_config.FOOTFALL_MULTIPLIER_LOW, analytics_config.FOOTFALL_MULTIPLIER_HIGH
    except ImportError:
        raise RuntimeError(
            "analytics_config.py not found. "
            "Copy analytics_config.example.py → analytics_config.py and fill in your values."
        )


def compute_derived(deal: dict) -> dict:
    m = deal["metrics"]
    engagement_rate  = (m["likes"] + m["comments"] + m["shares"] + m["saves"]) / max(m["total_reach"], 1)
    save_rate        = m["saves"] / max(m["total_reach"], 1)
    local_reach      = int(m["total_reach"] * m["audience_locality_match_pct"])
    action_rate      = (m["saves"] + m["link_clicks"] + m["profile_visits"]) / max(m["total_reach"], 1)

    # Footfall proxy calibrated against partner store counter data
    mult_low, mult_high = _load_footfall_multipliers()
    footfall_est_low  = int((m["saves"] + m["link_clicks"]) * mult_low)
    footfall_est_high = int((m["saves"] + m["link_clicks"]) * mult_high)

    return {
        "engagement_rate":   round(engagement_rate * 100, 2),
        "save_rate":         round(save_rate * 100, 2),
        "local_reach":       local_reach,
        "action_rate":       round(action_rate * 100, 2),
        "footfall_est_low":  footfall_est_low,
        "footfall_est_high": footfall_est_high,
    }


# ── Claude report ─────────────────────────────────────────────────────────────

def generate_report(deal: dict, derived: dict) -> str:
    client = anthropic.Anthropic()
    m = deal["metrics"]

    prompt = f"""You are writing a campaign performance report for a small local business owner in Bangalore.
They are not a marketer — keep language simple and direct. No jargon.

DEAL DETAILS:
Business: {deal['business_name']} ({deal['business_locality']})
Creator: {deal['creator_name']}
Post date: {deal['post_date']}
Campaign goal: {deal['campaign_goal']}

RAW METRICS:
- Total reach: {m['total_reach']:,} people
- Impressions: {m['impressions']:,}
- Likes: {m['likes']} | Comments: {m['comments']} | Shares: {m['shares']} | Saves: {m['saves']}
- Profile visits from post: {m['profile_visits']}
- Link/direction clicks: {m['link_clicks']}
- Audience in {deal['business_locality']}: {derived['local_reach']:,} people ({m['audience_locality_match_pct']*100:.0f}%)
- Engagement rate: {derived['engagement_rate']}%

Write a 150-word performance summary for the business owner. Include:
1. How many people it reached (especially locally)
2. What actions people took (saves, clicks — buying intent signals)
3. Estimated new visitors driven (use: {derived['footfall_est_low']}–{derived['footfall_est_high']} people)
4. One honest observation about what worked or what could improve
5. A clear recommendation: run again with the same creator, run again with a different creator, or pause

Tone: friendly, honest, numbers-first. Max 160 words."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


# ── Slack delivery ────────────────────────────────────────────────────────────

def post_report_to_slack(deal: dict, report: str) -> None:
    text = (
        f"*📊 Campaign Report — {deal['business_name']}*\n"
        f"Creator: {deal['creator_name']}  |  Post date: {deal['post_date']}\n\n"
        f"{report}"
    )
    requests.post(SLACK_WEBHOOK_URL, json={"text": text}, timeout=10).raise_for_status()


# ── Main ──────────────────────────────────────────────────────────────────────

def run_analyzer(deals: list[dict] | None = None) -> None:
    deals = deals or DEMO_DEALS
    print(f"\nDeal Performance Analyzer — {datetime.now().strftime('%Y-%m-%d')}")
    print("="*65)

    for deal in deals:
        print(f"\n▶ {deal['business_name']}  ×  {deal['creator_name']}")
        derived = compute_derived(deal)
        report  = generate_report(deal, derived)

        print(f"\n{report}\n")
        print("─"*65)

        if os.getenv("SLACK_ENABLED", "false").lower() == "true":
            post_report_to_slack(deal, report)


if __name__ == "__main__":
    run_analyzer()
