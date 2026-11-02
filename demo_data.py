"""
Demo deal performance data for the analyzer.
All data is synthetic — no real business names, creator IDs, or metrics.
"""

DEMO_DEALS = [
    {
        "deal_id":          "DEMO_DEAL_001",
        "business_id":      "DEMO_BIZ_001",
        "business_name":    "Demo Cafe Koramangala",
        "business_locality": "Koramangala",
        "creator_id":       "DEMO_CREATOR_001",
        "creator_name":     "Creator Alpha",
        "post_date":        "2024-10-15",
        "campaign_goal":    "Drive footfall to the cafe during weekday mornings",
        "metrics": {
            "total_reach":          4200,
            "impressions":          6800,
            "likes":                340,
            "comments":             28,
            "shares":               45,
            "saves":                130,
            "profile_visits":       210,
            "link_clicks":          88,
            "audience_city_match_pct": 0.71,
            "audience_locality_match_pct": 0.54,
        },
    },
    {
        "deal_id":          "DEMO_DEAL_002",
        "business_id":      "DEMO_BIZ_002",
        "business_name":    "Demo Fitness Studio HSR",
        "business_locality": "HSR Layout",
        "creator_id":       "DEMO_CREATOR_003",
        "creator_name":     "Creator Gamma",
        "post_date":        "2024-10-18",
        "campaign_goal":    "Get new class trial bookings for HIIT sessions",
        "metrics": {
            "total_reach":          6200,
            "impressions":          9400,
            "likes":                520,
            "comments":             44,
            "shares":               88,
            "saves":                210,
            "profile_visits":       380,
            "link_clicks":          145,
            "audience_city_match_pct": 0.80,
            "audience_locality_match_pct": 0.68,
        },
    },
    {
        "deal_id":          "DEMO_DEAL_003",
        "business_id":      "DEMO_BIZ_003",
        "business_name":    "Demo Home Decor Store JP Nagar",
        "business_locality": "JP Nagar",
        "creator_id":       "DEMO_CREATOR_004",
        "creator_name":     "Creator Delta",
        "post_date":        "2024-10-20",
        "campaign_goal":    "Show products in a real home setting, drive store visits",
        "metrics": {
            "total_reach":          1600,
            "impressions":          2400,
            "likes":                190,
            "comments":             22,
            "shares":               38,
            "saves":                95,
            "profile_visits":       140,
            "link_clicks":          52,
            "audience_city_match_pct": 0.85,
            "audience_locality_match_pct": 0.79,
        },
    },
]

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/DEMO_WEBHOOK_URL"
DAG_OWNER         = "demo-owner@demo.com"
