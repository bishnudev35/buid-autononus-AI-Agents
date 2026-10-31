
from gemini_model import generate_text_basic
from sample_function import get_weather
from prompts import react_system_prmpt
from json_helpers import extract_json

# Available actions
available_action = {
    "get_weather": get_weather
}

# User question
prompt = "Should I take an umbrella when going out today in mumbai?"

# Step 1: Ask Gemini to reason and select an action
response = generate_text_basic( prompt,system_prompt=react_system_prmpt)

# print("\nModel Response:\n", response)

# Step 2: Extract JSON from model response
json_function = extract_json(response)

if json_function:

    # Handle both list and dictionary outputs
    if isinstance(json_function, list):
        json_function = json_function[0]

    function_name = json_function.get("function_name")

    # Support the earlier misspelled parameter key
    function_params = (
        json_function.get("function_params")
        or json_function.get("function_prams")
    )

    # Step 3: Correct known function-name typo
    function_name_corrections = {
        "get_werather": "get_weather"
    }

    function_name = function_name_corrections.get(
        function_name,
        function_name
    )

    # Step 4: Validate action
    if function_name not in available_action:
        raise Exception(f"Unknown action: {function_name}")

    if not isinstance(function_params, dict):
        raise Exception("Invalid function parameters")

    print(f"\n-- Running {function_name}{function_params}")

    # Step 5: Execute function
    action_function = available_action[function_name]

    result = action_function(**function_params)

    print("\n-- Observation:", result)

    # Step 6: Send observation back to Gemini
    final_prompt = f"""
    User Question: {prompt}

    Action Executed: {function_name}

    Observation: {result}

    Based on the observation, answer the user's original question.
    Do not call any more tools.
    Give a clear and helpful answer.
    """

    final_response = generate_text_basic(
        final_prompt,
        system_prompt="You are a helpful AI assistant."
    )

    print("\nFinal Answer:\n", final_response)

else:
    print("\nNo valid action found.")
    print("Response:", response)
