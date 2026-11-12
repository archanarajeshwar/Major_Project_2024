import os

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Set the OPENAI_API_KEY environment variable before starting the application.")
