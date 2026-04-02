import requests
import time

class TargetModel:
    def __init__(
        self,
        base_url="http://localhost:8000/v1/completions",
        model_name="epfl-llm/meditron-7b",
        timeout=120,
        max_retries=3,
    ):
        self.base_url = base_url
        self.model_name = model_name
        self.timeout = timeout
        self.max_retries = max_retries

    def generate(self, prompt):

        formatted_prompt = f"""User: {prompt}
Assistant:"""

        payload = {
            "model": self.model_name,
            "prompt": formatted_prompt,
            "temperature": 0.2,
            "top_p":0.9,
            "max_tokens":512,
            "stop":["User:"]
        }

        for attempt in range(self.max_retries):

            try:

                response = requests.post(
                    self.base_url,
                    json=payload,
                    timeout=self.timeout
                )

                response.raise_for_status()

                data = response.json()

                text = data["choices"][0]["text"].strip()

                if text == "":
                    return "EMPTY_RESPONSE"

                return text

            except Exception:

                if attempt < self.max_retries-1:

                    wait_time = 5*(2**attempt)
                    time.sleep(wait_time)

                else:

                    return "EMPTY_RESPONSE"