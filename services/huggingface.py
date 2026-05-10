import os
import pdfplumber
import io
from huggingface_hub import InferenceClient
from services.model import ModelService


class HuggingFaceService(ModelService):
    def __init__(self):
        self.client = InferenceClient(token=os.environ.get("WPT_HF_API_KEY"))
        #self.model  = "meta-llama/Llama-3.1-8B-Instruct"
        #self.model = "Qwen/Qwen2.5-7B-Instruct"
        #self.model = "mistralai/Mistral-7B-Instruct-v0.3"
        #self.model = "HuggingFaceH4/zephyr-7b-beta"
        self.model = "deepseek-ai/DeepSeek-V4-Pro"

    def _extract_text(self, data):
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            return "".join(
                page.extract_text() for page in pdf.pages if page.extract_text()
            )

    def generate(self, prompt, documents):
        return self.generate_chat_completion(prompt, documents)

    def generate_text_generation(self, prompt, documents):
        doc_texts = "".join(
            f"### {doc['title']} ###\n{self._extract_text(doc['data'])}"
            for doc in documents
        )

        full_prompt = f"{doc_texts}\n\n{prompt}"

        response = self.client.text_generation(
            full_prompt,
            model=self.model,
            max_new_tokens=1024,
        )

        return response

    def generate_chat_completion(self, prompt, documents):
        doc_texts = "".join(
            f"### {doc['title']} ###\n{self._extract_text(doc['data'])}"
            for doc in documents
        )

        full_prompt = f"{doc_texts}\n\n{prompt}"

        response = self.client.chat_completion(
            messages=[{"role": "user", "content": full_prompt}],
            model=self.model,
            max_tokens=1024,
        )

        return response.choices[0].message.content
