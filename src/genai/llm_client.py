import os
from dotenv import load_dotenv

load_dotenv()


def get_llm_response(prompt):
    try:
        from google import genai

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=prompt
        )

        return response.text

    except Exception:
        # ❌ No static text anymore
        return None