import io
import json
import urllib.request
import pdfplumber
from services.model import ModelService

OLLAMA_URL = "http://localhost:11434/api/chat"


class OllamaService(ModelService):
    def __init__(self):
        self.model = "qwen2.5"

    def _extract_text(self, data):
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            return "".join(
                page.extract_text() for page in pdf.pages if page.extract_text()
            )

    def generate(self, prompt, documents):
        doc_texts = "".join(
            f"### {doc['title']} ###\n{self._extract_text(doc['data'])}"
            for doc in documents
        )

        full_prompt = f"{doc_texts}\n\n{prompt}"

        payload = json.dumps({
            "model":    self.model,
            "messages": [{"role": "user", "content": full_prompt}],
            "stream":   False,
            "options":  {"num_ctx": 32768},
        }).encode("utf-8")

        req      = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})
        response = urllib.request.urlopen(req)
        data     = json.loads(response.read().decode("utf-8"))

        return data["message"]["content"]
