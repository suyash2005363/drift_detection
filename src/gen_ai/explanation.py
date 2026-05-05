from .prompt_builder import build_drift_explanation_prompt
from .llm_client import get_llm_response

def generate_explanation(drift_results, drift_percentage, confidence):
    prompt = build_drift_explanation_prompt(
        drift_results, drift_percentage, confidence
    )
    return get_llm_response(prompt)