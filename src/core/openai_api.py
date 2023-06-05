import os

import openai
from dotenv import load_dotenv

from common.config import config

openai_config = config.openai


class Chatbot:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        self.messages = [{"role": "system", "content": openai_config.role}]

    def ask(self, question):
        self.messages.append({"role": "user", "content": question})

        response = openai.ChatCompletion.create(
            model=openai_config.model, messages=self.messages
        )
        
        reply = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": reply})

        return reply
