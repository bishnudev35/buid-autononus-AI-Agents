#react agent behalf of prompt

from gemini_model import generate_text_basic
from sample_function import get_weather
from prompts import react_system_prmpt
#availabel actions are:
available_action={
    "get_weather":get_weather
}

prompt=""" shoud i take an umbrela when goin out today in kolkata ?"""
response=generate_text_basic(prompt,system_prompt=react_system_prmpt)
print("Question: ",prompt)
print("Answer: ",response)