import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
import pdfplumber

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


def build_prompt(role, name, education, skills, projects):
    return f"""
You are a career mentor for engineering students in India.

Student profile:
- Name: {name}
- Education: {education}
- Skills known: {skills}
- Projects done: {projects}
- Target role: {role}

Respond ONLY with valid JSON (no markdown, no backticks, no extra text) in exactly this structure:

{{
  "skill_gap": ["list of specific missing skills for this role"],
  "roadmap": ["ordered list of things to learn, step by step"],
  "study_plan": {{
    "Week 1": "what to focus on",
    "Week 2": "what to focus on",
    "Week 3": "what to focus on",
    "Week 4": "what to focus on"
  }},
  "interview_questions": ["5 to 8 likely interview questions for this role, based on this profile"]
}}
"""


def call_ai_and_parse(prompt):
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json", "", 1).strip()
    return json.loads(raw_text)


@app.route("/generate-roadmap", methods=["POST"])
def generate_roadmap():
    try:
        data = request.get_json()

        role = data.get("role", "")
        name = data.get("name", "")
        education = data.get("education", "")
        skills = data.get("skills", "")
        projects = data.get("projects", "")

        prompt = build_prompt(role, name, education, skills, projects)
        result = call_ai_and_parse(prompt)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error_type": type(e).__name__, "error_message": str(e)}), 200


@app.route("/generate-roadmap-resume", methods=["POST"])
def generate_roadmap_resume():
    try:
        role = request.form.get("role", "")
        resume_file = request.files.get("resume")

        if not resume_file:
            return jsonify({"error": "No resume file received"}), 200

        # Extract text from the uploaded PDF
        resume_text = ""
        with pdfplumber.open(resume_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    resume_text += page_text + "\n"

        if not resume_text.strip():
            return jsonify({"error": "Could not read any text from that PDF. Try a different file."}), 200

        prompt = f"""
You are a career mentor for engineering students in India.

Below is the raw text extracted from a student's resume:
---
{resume_text}
---

Target role: {role}

Based on this resume and target role, respond ONLY with valid JSON (no markdown, no backticks, no extra text) in exactly this structure:

{{
  "skill_gap": ["list of specific missing skills for this role"],
  "roadmap": ["ordered list of things to learn, step by step"],
  "study_plan": {{
    "Week 1": "what to focus on",
    "Week 2": "what to focus on",
    "Week 3": "what to focus on",
    "Week 4": "what to focus on"
  }},
  "interview_questions": ["5 to 8 likely interview questions for this role, based on this profile"]
}}
"""

        result = call_ai_and_parse(prompt)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error_type": type(e).__name__, "error_message": str(e)}), 200


if __name__ == "__main__":
    app.run(debug=True)