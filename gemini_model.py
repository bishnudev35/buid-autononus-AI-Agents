
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini client
gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_text_basic(
    prompt: str,
    model="gemini-3.5-flash-lite",
    system_prompt: str = "You are helpful"
):
    response = gemini_client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "system_instruction": system_prompt
        }
    )

    return response.text
 