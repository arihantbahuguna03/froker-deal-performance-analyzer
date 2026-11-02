# Froker Deal Performance Analyzer

Weekly Airflow job that reads post metrics for each completed creator–business deal and uses Claude 3.5 Sonnet to write a plain-English performance report — automatically delivered to the business owner every Monday morning.

> Built Aug 2024 – Aug 2025 using Claude 3.5 Sonnet API directly — before MCP and modern agentic tooling existed in production-ready form. All orchestration is raw Airflow + Python.

---

## Problem

A creator posts for a local business on Froker. The business owner gets a link to an Instagram post. That's it. No metrics, no explanation, no verdict on whether it worked.

**Result:** Businesses can't tell if Froker campaigns drive real value. They don't renew. Froker loses its commission revenue. The creator-business relationship ends after one deal.

---

## Solution

Every Monday, Claude reads the raw post metrics for each deal from the previous week and writes a 150-word plain-English summary for the business owner:

- How many people saw the post (especially locally)
- What intent-signals people showed (saves, clicks, profile visits)
- Estimated footfall impact (saves + link clicks × conversion benchmark)
- One honest observation about what worked or what to improve
- A clear recommendation: run again same creator / try different creator / pause

**No dashboards to learn. No metrics to interpret. Just: here's what happened, here's what to do next.**

---

## Architecture

```
Airflow (every Monday 9am)
    └── PythonOperator
            ├── Fetch deals closed in previous 7 days
            ├── Compute derived metrics per deal
            │     (engagement rate, save rate, local reach, footfall estimate)
            ├── Claude 3.5 Sonnet — generate plain-English report per deal
            └── Post report to Slack (internal) + business notification
```

---

## Files

| File | Description |
|---|---|
| `performance_analyzer.py` | Metric computation + Claude report generation + Slack delivery |
| `dag.py` | Airflow DAG — weekly Monday 9am schedule |
| `demo_data.py` | Demo deal data with realistic metrics |
| `requirements.txt` | Dependencies |

---

## Sample Report (Claude output)

```
Campaign Report — Demo Cafe Koramangala
Creator: Creator Alpha  |  Post date: Oct 15, 2024

Your campaign reached 4,200 people, of whom 2,268 (54%) are in Koramangala
— the area right around your cafe. That's strong local targeting.

The clearest sign of interest: 130 people saved the post and 88 clicked
your profile link. Saves mean people want to come back to it later. Based
on these numbers, we estimate 33–58 new visitors to the cafe came from
this campaign.

What worked: Creator Alpha's tone matched your vibe — warm and honest,
not promotional. The morning coffee content resonated.

What to improve: The post went up on a Tuesday afternoon. Your audience
is most active on weekends. Next time, schedule for Saturday morning.

Recommendation: Run again with Creator Alpha. Same brief, weekend timing.
```

---

## Run locally

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
python performance_analyzer.py
```

---

## Design Decisions

| Decision | Reasoning |
|---|---|
| Claude writes the report, not a template | Templates produce generic text businesses ignore. Claude adapts to each deal's specific numbers and context |
| Footfall estimate as a range | Giving "43 visitors" sounds precise and untrustworthy. A range (33–58) is honest and more credible |
| Delivered Monday morning | Business owners think about their week on Monday. A Friday report gets buried |
| Saves + link clicks as intent proxy | Unlike likes, saves and direction clicks require deliberate action — they are the closest available proxy for offline purchase intent |
| Raw Anthropic SDK | Built Aug 2024 — no stable orchestration framework. Direct API gives full control over prompt and output format |
