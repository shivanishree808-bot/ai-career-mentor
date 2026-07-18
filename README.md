# AI Career Mentor for Students

An AI-powered career mentor built for the Idea2Impact 2026 Hackathon (Theme: Sustainability & Social Impact).

## Problem
Engineering students, especially freshers, struggle to enter the job market. Many don't know how to build a resume, don't know which jobs fit their skill level, and get overwhelmed by generic advice on social media.

## Solution
Students either upload their resume (PDF) or fill a short guided form. The AI (Google Gemini) then generates:
- A skill-gap analysis for their target role
- A personalized learning roadmap
- A 4-week study plan
- Likely interview questions

## Tech Stack
- Frontend: HTML, CSS, Bootstrap
- Backend: Python, Flask
- AI: Google Gemini API
- PDF parsing: pdfplumber

## Setup
1. Clone this repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with `GEMINI_API_KEY=your_key_here`
4. Run: `python app.py`
5. Visit `http://127.0.0.1:5000`