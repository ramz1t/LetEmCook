import os

import mistralai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
model = "ministral-3b-latest"
client = mistralai.Mistral(api_key=api_key)

history: dict[str, str] = {}

def generate_enhanced_text(original_text: str) -> str:
    content = (
        f"You are working as a text enhancer for the recipes app. "
        f"You are given an original text for the recipe description provided by the user. "
        f"Your job is to enhance the description and write detailed cooking steps. "
        f"Do not include the title or any welcoming phrases. "
        f"Here is the given text:\n\n{original_text}\n\n"
        f"Follow the steps: "
        f"Enhance recipe description. "
        f"Write detailed cooking steps. "
        f"Write ingredients list. "
        f"For each ingredient, specify the exact quantity in grams or milliliters. "
        f"Ensure the ingredients list is always the last section of the text. "
        f"Keep it short and informative."
    )
    return get_client_chat_completion_content(content)

def get_client_chat_completion_content(content: str) -> str:
    if content not in history:
        try:
            chat_response = client.chat.complete(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": content,
                    },
                ]
            )
            history[content] = chat_response.choices[0].message.content
        except mistralai.models.sdkerror.SDKError:
            raise ConnectionError("No API key provided. Check .env file or create a new key at https://console.mistral.ai/api-keys")

    return history[content]