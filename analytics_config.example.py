"""
Deal Analytics Config — Example
=================================
Copy this file to analytics_config.py and fill in your calibrated values.
analytics_config.py is gitignored — this example shows the structure only.

The footfall multipliers estimate real-world store visits from digital
engagement signals (saves + link clicks). Calibrated against foot-traffic
data from partner businesses using store counters and QR code redemptions.
"""

# ── Footfall estimation multipliers ──────────────────────────────────────────
# Rough estimate of real-world visits driven per (save + link_click).
# Low and high bounds give the business owner a range rather than a false point.
# Calibration: proprietary — available on request.
FOOTFALL_MULTIPLIER_LOW  = None   # conservative estimate
FOOTFALL_MULTIPLIER_HIGH = None   # optimistic estimate
