import os
import base64
import anthropic
from services.model import ModelService


class ClaudeService(ModelService):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("WPT_CLAUDE_API_KEY"))
        self.model  = "claude-sonnet-4-6"

    def generate(self, prompt, documents):
        content = []

        for doc in documents:
            content.append({
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": base64.standard_b64encode(doc["data"]).decode("utf-8"),
                },
                "title": doc["title"],
            })

        content.append({"type": "text", "text": prompt})

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": content}],
        )

        return message.content[0].text
