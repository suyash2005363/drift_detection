def build_drift_explanation_prompt(drift_results, drift_percentage, confidence):
    return f"""
You are an expert ML monitoring assistant.

Analyze the following drift detection results:

Drift Results:
{drift_results}

Drift Percentage: {drift_percentage}%
Model Confidence: {confidence}

Provide:
1. What drift has occurred
2. Which features are most affected
3. Possible real-world reasons
4. Impact on model performance
5. Recommended next steps

Keep explanation simple and clear for non-technical users.
"""
def build_risk_assessment_prompt(drift_percentage, confidence):
    return f"""
You are an AI risk analyst.

Given:
- Drift Percentage: {drift_percentage}%
- Model Confidence: {confidence}

Classify system status into:
- LOW RISK
- MEDIUM RISK
- HIGH RISK

Explain why and suggest action.

Keep answer short and professional.
"""

def build_report_prompt(drift_results, drift_percentage, confidence):
    return f"""
Generate a professional ML monitoring report.

Include:
- Summary of drift
- Key affected features
- Model reliability
- Business impact
- Recommendations

Data:
Drift Results: {drift_results}
Drift: {drift_percentage}%
Confidence: {confidence}

Write in report format.
"""