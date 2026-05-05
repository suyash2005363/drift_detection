def generate_explanation(drift_results, drift_percentage, confidence):

    drifted_features = [
        feature for feature, details in drift_results.items()
        if details.get("drift_detected") is True
    ]

    total = len(drift_results)
    count = len(drifted_features)

    top_features = ", ".join(drifted_features[:3])

    # ✅ Severity logic
    if drift_percentage > 40:
        severity = "HIGH"
        impact = "Model performance is likely severely affected."
        recommendation = "Immediate retraining is recommended."
    elif drift_percentage > 20:
        severity = "MEDIUM"
        impact = "Model reliability may degrade over time."
        recommendation = "Monitor closely and plan retraining."
    else:
        severity = "LOW"
        impact = "Minor drift detected with limited impact."
        recommendation = "No immediate action required."

    return f"""
AI Explanation:

Drift detected in {count} out of {total} features ({drift_percentage:.2f}%).

Severity Level: {severity}

Most affected features:
{top_features}

Possible causes:
- Change in user behavior
- Data collection differences
- Seasonal or demographic shifts

Impact:
{impact}

Recommendation:
{recommendation}
"""