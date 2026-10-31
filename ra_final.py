
from gemini_model import generate_text_with_conversation
from sample_function import get_weather
from prompts import react_system_prmpt
from json_helpers import extract_json

# Available actions
available_action = {
    "get_weather": get_weather
}

# Conversation history
messages = [
    {"role": "system", "content": react_system_prmpt}
]

max_turns = 5

# Function name corrections for older model outputs.
function_name_corrections = {
    "get_werather": "get_weather",
    "get weather": "get_weather",
}

# Conversation loop
print("Chat started. Type 'exit', 'quit', or 'q' to stop.")

while True:
    try:
        prompt = input("\nYou: ").strip()
    except EOFError:
        print("\nGoodbye!")
        break

    if prompt.casefold() in {"exit", "quit", "q"}:
        print("Goodbye!")
        break

    if not prompt:
        print("Please enter a question.")
        continue

    messages.append({"role": "user", "content": prompt})
    turn_count = 1
    answered = False

    # ReAct loop for the current user question
    while turn_count <= max_turns:

        print(f"\nLoop: {turn_count}")
        print("-----------------------")

        # Step 1: Ask Gemini
        response = generate_text_with_conversation(messages)

        print("\nAssistant:")
        print(response)

        # Add model response to conversation history
        messages.append({
            "role": "assistant",
            "content": response
        })

        # Step 2: Extract JSON
        json_function = extract_json(response)

        # Step 3: Check whether the model wants to call a tool
        if not json_function:
            answered = True
            break

        # Handle dictionary or list output
        if isinstance(json_function, list):
            if not json_function:
                print("No valid action found.")
                break
            json_function = json_function[0]

        # Step 4: Extract function details
        if not isinstance(json_function, dict):
            print("Invalid action format: expected a JSON object.")
            break

        function_name = json_function.get("function_name")

        function_params = (
            json_function.get("function_params")
            or json_function.get("function_prams")
        )

        # Correct known typo
        function_name = function_name_corrections.get(
            function_name,
            function_name
        )

        # Step 5: Validate function
        if function_name not in available_action:
            print(f"Unknown action: {function_name!r}")
            break

        if not isinstance(function_params, dict):
            print("Invalid function parameters: expected a JSON object.")
            break

        print(f"\n-- Running {function_name}{function_params}")

        # Step 6: Execute function
        action_function = available_action[function_name]

        try:
            result = action_function(**function_params)

        except Exception as e:
            result = f"Tool execution failed: {str(e)}"

        print("\n-- Observation:")
        print(result)

        # Step 7: Add observation to conversation history
        messages.append({
            "role": "user",
            "content": f"""
        Observation from tool {function_name}:

        {result}

        Based on this observation:
        - If another tool is required, return the next Action JSON.
        - Otherwise, provide the final answer to the original question.
        """
        })

        turn_count += 1

    if not answered and turn_count > max_turns:
        print("\nMaximum turns reached for this question.")
