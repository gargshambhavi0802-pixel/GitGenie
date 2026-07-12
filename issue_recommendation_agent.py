import requests
import os
import json
from dotenv import load_dotenv
from google import genai
from groq import Groq

# Load environment variables
load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

if not gemini_key:
    raise ValueError("GEMINI_API_KEY not found.")

client = genai.Client(api_key=gemini_key)

groq_client = None
if groq_key:
    groq_client = Groq(api_key=groq_key)


def fetch_repository(repo_name):
    """
    Fetch repository information from GitHub.
    """

    url = f"https://api.github.com/repos/{repo_name}"

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as e:
        print("GitHub Request Failed:", e)
        return None

    if response.status_code != 200:
        print("Repository not found.")
        return None

    data = response.json()

    return {
        "name": data.get("name"),
        "owner": data.get("owner", {}).get("login"),
        "description": data.get("description"),
        "language": data.get("language"),
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "topics": data.get("topics", []),
        "url": data.get("html_url")
    }

def fetch_readme(repo_name):
    """
    Fetch README content from GitHub.
    """

    url = f"https://api.github.com/repos/{repo_name}/readme"

    headers = {
        "Accept": "application/vnd.github.raw+json"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )
    except requests.RequestException:
        return ""

    if response.status_code == 200:
        return response.text

    return ""


def fetch_issues(repo_name):
    """
    Fetch open issues from GitHub.
    Ignore pull requests.
    """

    url = (
        f"https://api.github.com/repos/"
        f"{repo_name}/issues"
        "?state=open&per_page=20"
    )

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        return []

    if response.status_code != 200:
        return []

    issues = response.json()

    issue_list = []

    for issue in issues:

        # Skip pull requests
        if "pull_request" in issue:
            continue

        issue_list.append(
            {
                "title": issue.get("title"),
                "body": issue.get("body", ""),
                "labels": [
                    label["name"]
                    for label in issue.get("labels", [])
                ],
                "url": issue.get("html_url")
            }
        )

    return issue_list

def recommend_issues(repo, readme, issues):

    prompt = f"""
You are an Open Source Mentor.

Repository Information:
{json.dumps(repo, indent=2)}

README:
{readme[:4000]}

Open Issues:
{json.dumps(issues, indent=2)}

Task:
Recommend the top beginner-friendly issues.

For each issue provide:
- Issue Title
- Difficulty (Easy/Medium/Hard)
- Why it is suitable
- Skills Required
- Estimated Time
- Learning Outcome

Return the result in clean Markdown.
"""

    # ---------- Try Gemini ----------
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as gemini_error:

        print("\nGemini failed. Trying Groq...\n")

        # ---------- Fallback to Groq ----------
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

def main():

    print("=" * 70)
    print("        ISSUE RECOMMENDATION AGENT")
    print("=" * 70)

    repo_name = input(
        "\nEnter GitHub Repository (owner/repo): "
    ).strip()

    repo = fetch_repository(repo_name)

    if repo is None:
        return

    print("\nFetching repository details...\n")

    readme = fetch_readme(repo_name)
    issues = fetch_issues(repo_name)

    if len(issues) == 0:
        print("No open issues found.")
        return

    print("Generating AI Recommendations...\n")

    recommendations = recommend_issues(
        repo,
        readme,
        issues
    )

    print("=" * 70)
    print("ISSUE RECOMMENDATIONS")
    print("=" * 70)
    print(recommendations)


if __name__ == "__main__":
    main()
