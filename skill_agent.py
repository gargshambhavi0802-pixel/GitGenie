from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def generate_profile():

    user_skills = input("Enter your programming skills (comma separated): ")
    experience = input("Enter your experience level (Beginner/Intermediate/Advanced): ")
    domain = input("Which domain interests you? (Web Development, AI/ML, App Development, Data Science, etc.): ")

    prompt = f"""
You are an experienced career mentor.

Analyze the following user information and create a structured profile.

Programming Skills:
{user_skills}

Experience Level:
{experience}

Interested Domain:
{domain}

Return ONLY a valid JSON object with the following structure:

{{
    "languages": [],
    "experience_level": "",
    "interests": [],
    "strengths": [],
    "recommended_learning_path": []
}}

Rules:
- Return ONLY valid JSON.
- Do NOT include markdown formatting.
- Do NOT include triple backticks.
- Do NOT write ```json.
- Do NOT add any explanation before or after the JSON.
- Keep "languages" and "interests" as arrays.
- Keep "experience_level" as a single string.
- Generate 3-5 strengths based on the user's profile.
- Generate a practical learning path in logical order.
"""

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
    )

    try:
        profile = json.loads(response.text)   #Take this JSON text and convert it into a Python dictionary
    except json.JSONDecodeError:
        print("Gemini returned invalid JSON.")
        return None
    
    return profile

if __name__ == "__main__":

    profile = generate_profile()

    print("\nUser Profile\n")

    print(json.dumps(profile, indent=4))