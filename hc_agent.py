#hardcoded agent

from gemini_model import generate_text_basic
from sample_function import get_weather

current_weather=get_weather("kolkata")

prompt=f""" 
shoud i take an umbrela when goin out today in kolkata based on the 
following weather condintion: {current_weather}?"""
response=generate_text_basic(prompt)
print("Question: ",prompt)
print("Answer: ",response)