# AP Physics 2 Quiz App!
import requests
import json
import csv
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MY_API_KEY")

URL = (
    "https://generativelanguage.googleapis.com"
    "/v1beta/models/gemini-2.5-flash:generateContent"
    f"?key={API_KEY}"
)

def get_unit():
    """User selects the unit they want to practice. They input the number of the unit."""
    print("Please select the AP Physics 2 unit you want to practice. Type in the unit NUMBER!")
    print("9.  Thermodynamics")
    print("10. Electric Force, Field, and Potential")
    print("11. Electric Circuits")
    print("12. Magnetism and Electromagnetism")
    print("13. Geometric Optics")
    print("14. Waves, Sound, and Physical Optics")
    print("15. Modern Physics")
    unit = int(input("Type the number of the unit you want to practice here: "))
    return unit

def get_weak_skills():
    """Get the user's weakest skills and types DONE when they are done."""
    print("Type in you weakest skills (dervies, calculations, experimental design, etc.)")
    print("Press enter after each skill and type DONE when you're done!")
    skills = []
    while True:
        skill = input("  - ")
        if skill.strip().lower() == "done":
            break
        skills.append(skill)
    return ", ".join(skills)

def create_quiz(unit, skills):
    """Takes the user's chosen unit and skills and creates 5 MCQ"""
    prompt = f""" Using the student's weakest skills and chosen AP Physics 2 unit, generate 5 multiple choice questions to study for the AP Physics 2 exam.
    Each question must have options A, B, C, and D only.
    
    These are the AP Physics 2 units:
    9. Thermodynamics
    10. Electric Force, Field, and Potential
    11. Electric Circuits
    12. Magnetism and Electromagnetism
    13. Geometric Optics
    14. Waves, Sound, and Physical Optics
    15. Modern Physics
     
    The chosen unit: {unit}
    The student's weakest skills: {skills}

    Respond with only a valid JSON array in this exact format:
    [
        {{
            "question": "How does...?",
            "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
            "answer": "B"
            "explanation": "The answer is B because..."
        }}
    ]
    """
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(URL, json=body, timeout=25)
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
        print("Error:", e)
        return None

def take_quiz(questions):
    """Shows the user questions and gives the answer and explanation"""
    score = 0
    results = []
    for i, question in enumerate(questions, 1):
        print(f"Question {i}")
        print(question["question"])
        for option in question["options"]:
            print(f"   {option}")
            
        user_answer = input("Your answer: ").strip().upper()
        if user_answer == question["answer"]:
            print(f"Correct! Here is an explanation: {question["explanation"]}")
            score += 1
        else:
            print(f"Wrong! The answer was {question["answer"]}. Here is an explanation: {question["explanation"]}")
        
        user_option = ""
        correct_option = ""
        for option in question["options"]:
            if option[0] == user_answer:
                user_option = option
            if option[0] == question["answer"]:
                correct_option = option
                
        results.append({
            "question": question["question"],
            "user_option": user_option,
            "correct_option": correct_option,
            "explanation": question["explanation"]
        })
    print(f"Score: {score}/5")
    return results

def save_quiz(results):
    """Saves the questions, user's answers, correct answers, and explanations in a CSV file"""
    file_exists = os.path.exists("quiz_answers.csv")
    with open("quiz_answers.csv", "a", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["question", "user_option", "correct_option", "explanation"])
        if not file_exists:
            writer.writeheader()
        for result in results:
            writer.writerow({
                "question": result["question"],
                "user_option": result["user_option"],
                "correct_option": result["correct_option"],
                "explanation": result["explanation"]
            })
    print("Quiz saved!")

def main():
    print("WELCOME TO THE AP PHYSICS 2 QUIZ APP!")
    print()
    unit = get_unit()
    skills = get_weak_skills()
    print("Creating your quiz...")
    questions = create_quiz(unit, skills)
    results = take_quiz(questions)
    save_quiz(results)

if __name__ == "__main__":
    main()