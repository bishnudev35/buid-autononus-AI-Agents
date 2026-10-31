
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

def generate_text_with_conversation(messages, model="gemini-3.5-flash-lite"):
    """Generate a response from OpenAI-style conversation messages.

    ``google-genai`` uses ``contents`` and the assistant role is named
    ``model``.  Convert the small message format used by the agent before
    sending it to the SDK, and pass the system message separately.
    """
    system_instruction = next(
        (message["content"] for message in messages
         if message.get("role") == "system"),
        "You are helpful.",
    )
    contents = [
        {
            "role": "model" if message.get("role") == "assistant" else "user",
            "parts": [{"text": str(message.get("content", ""))}],
        }
        for message in messages
        if message.get("role") != "system"
    ]
    response=gemini_client.models.generate_content(
        model=model,
        contents=contents,
        config={"system_instruction": system_instruction},
    )
    return response.text
 
