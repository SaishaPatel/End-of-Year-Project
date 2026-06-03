# AP Physics 2 Quiz App!

# Imports
import requests
import json
import csv
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# API KEY
API_KEY = os.getenv("MY_API_KEY")

URL = (
    "https://generativelanguage.googleapis.com"
    "/v1beta/models/gemini-2.5-flash:generateContent"
    f"?key={API_KEY}"
)

# def get_base_dir():
#     """
#     Returns the folder where the program is running:
#     - If running as .py, it's the script folder
#     - If running as .exe (PyInstaller), it's the exe folder
#     """
#     if getattr(sys, "frozen", False):
#         # Running in PyInstaller bundle
#         return os.path.dirname(sys.executable)
#     else:
#         # Running as normal .py script
#         return os.path.dirname(os.path.abspath(__file__))

# Get the unit the student wants to practice
def get_unit():
    print("\nPlease select the AP Physics 2 unit you want to practice. Type in the unit NUMBER!")
    print("9. Thermodynamics")
    print("10. Electric Field, Force, and Potential")
    print("11. Electric Circuits")
    print("12. Magnetism and Electromagnetism")
    print("13. Optics")
    print("14. Waves, Sound, and Physical Optics")
    print("15. Modern Physics")
    unit = int(input("Type the number of the unit you want to practice here: "))
    return unit

# Get the weakest skills the student wants to practice
def get_weak_skills():
    """
    Get the users weakest skills. 
    One word inputs with multiple lines.
    User types END to complete this
    """
    print("Type in you weakest skills (dervies, calculations, experimental design, etc.)")
    print("Press enter after each skills and type END when you're done!")
    skills = []
    while True:
        skill = input("- ")
        if skill.strip().upper() == "END":
            break
        skills.append(skill)
    return "\n".join(skills)

# Create the quiz
def create_quiz(unit, skills):
    """Takes the skills the user inputs to Gemini and creates 5 MCQ"""
    prompt = f"""Based on the student's weakest skills and chosen AP Physics 2 unit, generate exactly \ 
    5 multiple choice questions to study for the AP Physics 2 exam.
    Each question MUST have exactly four choices labeled A, B, C, and D.

    The student's weakest skills:
    {skills}
    
    The chosen unit: 
    {unit}

    Respond with ONLY a valid JSON array in this exact format:
    [
        {{
            "question": "What is...?",
            "choices": ["A) ...", "B) ...", "C) ...", "D) ..."],
            "answer": "A"
            "explanation": "The answer is A because..."
        }}
    ]
    Only the JSON array. No extra text.
    """
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(URL, json=body, timeout=30)
        if response.status_code != 200:
            print(f"API error: {response.status_code}")
            return None
        data = response.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()

        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]

        return json.loads(text)
    except Exception as e:
        print("Error generating quiz:", e)
        return None

# Running the quiz app
def run_quiz(questions):
    """Shows the user questions, gives the answer/explanation, and takes these results"""
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\n Question {i} of 5")
        print(q["question"])

        for choice in q["choices"]:
            print(f"  {choice}")

        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        correct_answer = q["answer"]

        is_correct = user_answer == correct_answer

        if is_correct:
            print(f"Correct! Here is an explanation: {q["explanation"]}")
            score += 1
        else:
            print(f" Wrong — the answer was {correct_answer}. Here is an explanation: {q["explanation"]}")

        choice_a = q["choices"][0][3:]
        choice_b = q["choices"][1][3:]
        choice_c = q["choices"][2][3:]
        choice_d = q["choices"][3][3:]
        
        results = []
        results.append({
            "question": q["question"],
            "choice_a": choice_a,
            "choice_b": choice_b,
            "choice_c": choice_c,
            "choice_d": choice_d,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "explanation": q["explanation"],
            "result": "Correct" if is_correct else "Wrong"
        })

    print(f"\nScore: {score}/5 ({score / 5 * 100:.0f}%)")
    return score, results

# TESTING
unit = get_unit()
skill = get_weak_skills()
questions = create_quiz(unit, skill)
run_quiz(questions)