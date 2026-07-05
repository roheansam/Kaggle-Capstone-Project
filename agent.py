import os
from dotenv import load_dotenv
from google import genai

from prompts import PROJECT_AGENT_PROMPT
from guardrails import validate_project_idea

load_dotenv()


def generate_project_blueprint(user_idea: str):
    is_valid, message = validate_project_idea(user_idea)

    if not is_valid:
        return message

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return """
API key is missing.

Please open the .env file and add your Gemini API key like this:

GEMINI_API_KEY=your_actual_api_key_here
"""

    client = genai.Client(api_key=api_key)

    final_prompt = f"""
{PROJECT_AGENT_PROMPT}

User's project idea:
{user_idea}

Now generate the complete project blueprint.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=final_prompt
        )

        return response.text

    except Exception as error:
        return f"""
Something went wrong while generating the blueprint.

Error:
{error}

Possible fixes:
1. Check whether your Gemini API key is correct.
2. Check whether the selected Gemini model is available for your account.
3. Try changing the model name in agent.py.
"""