import os
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


def get_model_service():
    provider = os.environ.get("WPT_MODEL_PROVIDER", "CLAUDE").upper()
    if provider == "HF":
        from services.huggingface import HuggingFaceService
        return HuggingFaceService()
    if provider == "OLLAMA":
        from services.ollama import OllamaService
        return OllamaService()
    from services.claude import ClaudeService
    return ClaudeService()


with open("data/udl_guidelines.txt", "r") as f:
    udl_guidelines = f.read()

PROMPT = f"""
    You are an expert special education consultant.
    Review the student IEP and lesson plan provided.
    The IEP will contain the student's full name, extract it.
    The lesson will contain identification of the lesson topic, extract it.

    The IEP will contain areas that the student needs accommodation for.
    Accommodations are adjustments the teacher makes to deliver the lesson.
    Be specific to the lesson content.

    The IEP will also contain goals that the teacher could be evaluating
    during this lesson. Evaluations are specific moments in the lesson
    where the teacher can observe or measure the student's progress against
    an IEP goal — not generic observations.

    Each accommodation and evaluation must include a citation referencing:
    - the specific IEP goal or section it is drawn from
    - the specific part of the lesson plan it applies to

    All modifications should adhere to and take advantage of the following
    UDL (Universal Design for Learning) guidelines where applicable:

    {udl_guidelines}

    The resulting JSON should be:
    {{
      "student_name": <student full name from IEP>,
      "lesson": <description of this lesson>,
      "accommodations": [
        {{
          "action": <specific actionable adjustment for the teacher>,
          "iep_reference": <the IEP goal or section this addresses>,
          "lesson_reference": <the part of the lesson this applies to>
        }}
      ],
      "evaluations": [
        {{
          "observation": <specific moment in the lesson to observe or measure>,
          "iep_goal": <the IEP goal being evaluated>,
          "lesson_reference": <the part of the lesson this applies to>
        }}
      ]
    }}


    Citations should be kept brief but make clear the justification.

    Do NOT make generic recommendations. Every item must be grounded in
    both the IEP and the lesson plan. The priority should be on making
    recommendations based on the IEP for this specific lesson plan only
    and should not make reference to other lessons.

    Do not wrap the JSON in markdown code fences or backticks.
    No other text, just the JSON.
"""

PROMPT_VERSION = "IEPL 0.0.1"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    iep    = request.files.get("iep")
    lesson = request.files.get("lesson")

    if not iep or not lesson:
        return jsonify(error="Both files are required."), 400

    documents = [
        {"title": "Student IEP",  "data": iep.read()},
        {"title": "Lesson Plan",  "data": lesson.read()},
    ]

    service  = get_model_service()
    response = service.generate(PROMPT, documents)

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
