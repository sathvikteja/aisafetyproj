import google.generativeai as genai
from mistralai import Mistral
import time
from mistralai.models.sdkerror import SDKError

class GeminiAttacker:
    def __init__(self, api_key, model_name="gemini-2.5-flash", system_prompt=None):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name,
            system_instruction=system_prompt
        )

    def generate(self, system_prompt, user_prompt):
        response = self.model.generate_content(user_prompt)
        return response.text


class MistralAttacker:
    def __init__(self, api_key, model_name="mistral-large-latest", system_prompt=None):
        self.client = Mistral(api_key=api_key)
        self.model_name = model_name
        self.system_prompt = system_prompt

    def generate(self, system_prompt, user_prompt):

        for attempt in range(5):

            try:

                response = self.client.chat.complete(

                    model=self.model_name,

                    messages=[
                        {"role":"system","content":system_prompt},
                        {"role":"user","content":user_prompt}
                    ],

                    temperature=1.1,
                    max_tokens=800

                )

                return response.choices[0].message.content

            except SDKError as e:

                if "429" in str(e):

                    wait = 5 * (attempt + 1)

                    print(f"Rate limited. Sleeping {wait}s")

                    time.sleep(wait)

                else:
                    raise

        return None