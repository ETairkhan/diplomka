import os


class LLMAdapter:
    # One interface for any LLM (cloud or local), so the model can be changed
    # without changing the rest of the code.

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "")
        self.model = os.getenv("LLM_MODEL", "")
        self.api_key = os.getenv("LLM_API_KEY", "")

    def analyze(self, transcript):
        # call the selected LLM and return topics, scores and summary as JSON
        raise NotImplementedError("LLM is not selected yet")
