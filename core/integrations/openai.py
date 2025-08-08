import os
from dotenv import load_dotenv
from openai import OpenAI

class ExtendedOpenAI:
    def __init__(self):
        load_dotenv()

        # Accept either OpenRouter or OpenAI credentials
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "No API key found. Set OPENROUTER_API_KEY (for OpenRouter) or OPENAI_API_KEY (for OpenAI) in your environment or .env"
            )

        # Determine base_url
        base_url = os.getenv("BASE_URL")
        if not base_url:
            base_url = "https://openrouter.ai/api/v1"

        self.client = OpenAI(
            api_key=api_key
        )
        self.model = os.getenv("MODEL")

    def get_response(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

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