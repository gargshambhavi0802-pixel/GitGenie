import os
import requests
from dotenv import load_dotenv
from google import genai
from groq import Groq

# -------------------- Load Keys --------------------

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY_2")
groq_key = os.getenv("GROQ_API_KEY_2")

if not gemini_key:
    raise ValueError("GEMINI_API_KEY_2 not found.")

client = genai.Client(api_key=gemini_key)

groq_client = None
if groq_key:
    groq_client = Groq(api_key=groq_key)

# -------------------- GitHub --------------------

def get_repository(repo_name):
    url = f"https://api.github.com/repos/{repo_name}"

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as e:
        print("GitHub Request Failed:", e)
        return None

    if response.status_code != 200:
        print("Repository not found.")
        return None

    return response.json()


def get_contributing_file(repo_name):
    paths = [
        "CONTRIBUTING.md",
        ".github/CONTRIBUTING.md",
        "docs/CONTRIBUTING.md"
    ]

    for path in paths:
        url = f"https://api.github.com/repos/{repo_name}/contents/{path}"

        response = requests.get(
            url,
            headers={
                "Accept": "application/vnd.github.raw"
            }
        )

        if response.status_code == 200:
            return response.text

    return "CONTRIBUTING.md not found."


def get_pull_request(repo_name, pr_number):
    url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}"

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as e:
        print("GitHub Request Failed:", e)
        return None

    if response.status_code != 200:
        print("Pull Request not found.")
        return None

    pr = response.json()

    return {
        "title": pr.get("title", ""),
        "description": pr.get("body", "")
    }


def format_pr(pr):
    return f"""Title: {pr['title']}

Description:

{pr['description']}
"""

# -------------------- AI --------------------

def generate_checklist(contributing_rules, pr_text):

    prompt = f"""
You are an Open Source Code Review Assistant.

Repository Contribution Rules:

{contributing_rules}

Pull Request:

{pr_text}

Task:

Evaluate whether the Pull Request follows the contribution rules.

For every rule provide:

- Rule
- Status (✅ Followed / ❌ Not Followed / ⚠️ Cannot Verify)
- Reason

If CONTRIBUTING.md is missing, evaluate using common open-source best practices.

Return the result in clean Markdown.
"""

    # -------- Gemini --------
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as gemini_error:

        print("\nGemini failed. Trying Groq...\n")

        # -------- Groq Fallback --------
        if groq_client is not None:
            try:
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                return response.choices[0].message.content

            except Exception as groq_error:
                return f"""
Gemini Error:

{gemini_error}

Groq Error:

{groq_error}
"""

        return f"Gemini Error:\n{gemini_error}"

# -------------------- Main --------------------

def main():

    print("=" * 70)
    print("        CONTRIBUTION CHECKLIST AGENT")
    print("=" * 70)

    repo_name = input(
        "\nEnter GitHub Repository (owner/repo): "
    ).strip()

    pr_number = input(
        "Enter Pull Request Number: "
    ).strip()

    repository = get_repository(repo_name)

    if repository is None:
        return

    contributing_rules = get_contributing_file(repo_name)

    pull_request = get_pull_request(repo_name, pr_number)

    if pull_request is None:
        return

    pr_text = format_pr(pull_request)

    print("\n===== CONTRIBUTING RULES =====")
    print(contributing_rules)

    print("\n==============================")

    print("\n===== PR DESCRIPTION =====")
    print(pr_text)

    print("==========================")

    print("\nGenerating AI Checklist...\n")

    checklist = generate_checklist(
        contributing_rules,
        pr_text
    )

    print("===== AI CHECKLIST =====")
    print(checklist)


if __name__ == "__main__":
    main()