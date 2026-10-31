import re
import json

def extract_json(text_response):
    pattern = r'\{.*\}'

    match = re.search(pattern, text_response, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None

    return None
