import os
from dotenv import load_dotenv
from openai import OpenAI
import pathlib

class OpenRouter:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url=os.getenv("BASE_URL"))
        self.model = os.getenv("MODEL")

    def get_response(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    
    def get_response_with_context(self, prompt, context):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )

    # make it chainable with chain op
    def __call__(self, prompt) -> str:
        try:
            if not isinstance(prompt, str) and hasattr(prompt, "to_string"):
                prompt_text = prompt.to_string()
            else:
                prompt_text = str(prompt)
        except Exception:
            prompt_text = str(prompt)
        return self.get_response(prompt_text)