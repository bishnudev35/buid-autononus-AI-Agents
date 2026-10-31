# Autonomous AI Agents

This project is an educational collection of Python examples that demonstrate how to build AI agents with Gemini, ReAct-style reasoning, tool execution, JSON extraction, and multi-turn conversations.

The main agent accepts questions from the terminal, decides whether it needs the weather tool, executes that tool, and then uses the result to answer the user.

## Project goals

- Learn the basic structure of an AI agent.
- Separate prompts, model access, tools, and JSON parsing into individual modules.
- Experiment with single-turn, multi-turn, hard-coded, and tool-using agents.
- Compare direct Gemini SDK usage with the `SimplerLLM` abstraction.

## Requirements

- Python 3.10 or newer
- A Gemini API key
- Internet access for Gemini API requests

## Installation

Create and activate a virtual environment from the project directory:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the packages used by the examples:

```powershell
pip install google-genai python-dotenv SimplerLLM
```

If PowerShell does not allow activation, run the Python executable directly:

```powershell
.\venv\Scripts\python.exe ra_final.py
```

## Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The direct Gemini implementation loads this value through `python-dotenv`. `SimplerLLM` also expects the Gemini credentials to be available through the environment.

Never commit `.env` or expose your API key. These files are excluded by `.gitignore`.

## Run the main conversational agents

### Direct Gemini implementation

```powershell
python ra_final.py
```

This version uses `google-genai` directly through [gemini_model.py](./gemini_model.py). It maintains conversation history and allows up to five ReAct/tool turns for each question.

### SimplerLLM implementation

```powershell
python ra_fianl_simpler.py
```

The filename intentionally matches the existing project file, including the spelling `fianl`. This version uses `SimplerLLM` for model calls and JSON extraction.

During either chat, type a question at the `You:` prompt. To stop, enter any of:

```text
exit
quit
q
```

## Example

```text
Chat started. Type 'exit', 'quit', or 'q' to stop.

You: Should I take an umbrella when going out in Mumbai?
Assistant: Yes, you should take an umbrella because the sample weather is rainy.

You: q
Goodbye!
```

## How the ReAct loop works

1. The user enters a question.
2. The model receives the system prompt and conversation history.
3. The model either returns a final answer or emits an action JSON object.
4. The program validates the action and calls the matching Python function.
5. The tool result is added to the conversation as an observation.
6. The model receives the observation and produces the final answer.
7. The outer conversation loop waits for the next user question.

The expected action format is:

```json
{
  "function_name": "get_weather",
  "function_params": {
    "city": "Mumbai"
  }
}
```

## Project structure

| File | Description |
| --- | --- |
| `ra_final.py` | Main multi-turn agent using the direct Gemini client. |
| `ra_fianl_simpler.py` | Multi-turn agent using `SimplerLLM`. |
| `gemini_model.py` | Creates the Gemini client and provides basic and conversation helpers. |
| `prompts.py` | Contains the ReAct system prompt and action protocol. |
| `sample_function.py` | Contains the sample `get_weather` tool. |
| `json_helpers.py` | Extracts a JSON object from model output. |
| `ra_with_function_test.py` | Earlier single-question tool-calling example. |
| `react_agent_test.py` | Basic ReAct prompt experiment. |
| `hc_agent.py` | Hard-coded weather lookup followed by an LLM response. |
| `test.py` | Basic direct Gemini question example. |
| `.env` | Local API-key configuration; do not commit. |
| `.gitignore` | Excludes secrets, virtual environments, and Python cache files. |

## Weather tool

`get_weather(city)` is demonstration data, not a live weather service. It currently supports:

- Delhi: sunny
- Kolkata: sunny
- Mumbai: rainy
- Hyderabad: cloudy
- Bangalore: rainy

The function normalizes capitalization and supports several common spelling variations. Unknown cities produce a clear error instead of silently returning an empty result.

## Troubleshooting

### Missing API key

Confirm that `.env` exists in the project directory and contains `GEMINI_API_KEY`. Restart the terminal after changing environment variables.

### Package import error

Ensure the virtual environment is active and reinstall dependencies:

```powershell
pip install --upgrade google-genai python-dotenv SimplerLLM
```

### Model or API errors

Check that the configured Gemini model is available to your account and that your API key has access to it. The current examples use `gemini-3.5-flash-lite`.

### JSON action is not recognized

The model must return an action containing `function_name` and `function_params`. Review [prompts.py](./prompts.py) if the model output format changes.

## Development notes

- The weather values are static and should not be used for safety-critical decisions.
- The prompt, model wrapper, tools, and JSON parser are intentionally separate so they can be replaced independently.
- The agent catches tool exceptions and returns the error to the model as an observation.
- The maximum ReAct turn count prevents an accidental infinite tool loop.

## License

No license has been specified for this educational project.
