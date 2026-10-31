from gemini_model import generate_text_basic
prompt="whate are the todays tempareture in kolkata"
response=generate_text_basic(prompt)
print("Question: ",prompt)
print("Answer: ",response)