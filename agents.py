import os
from dotenv import load_dotenv
from crewai import Agent
from crew.fallback_llm import GeminiGroqFallbackLLM

load_dotenv()


# ============================
# Actual LLMs
# ============================



# ============================
# Gemini + Groq Fallback
# ============================
llm = GeminiGroqFallbackLLM()

# ============================
# Agents
# ============================


repository_recommender = Agent(
    role="Repository Recommendation Expert",
    goal="Recommend the best GitHub repositories for a user.",
    backstory="Expert in matching developers with suitable open source repositories.",
    llm=llm,
    verbose=True
)


repository_explainer = Agent(
    role="Repository Explainer",
    goal="Explain GitHub repositories in beginner friendly language.",
    backstory="Expert software architect who simplifies complex repositories.",
    llm=llm,
    verbose=True
)


skill_analyzer = Agent(
    role="Skill Analyzer",
    goal="Analyze user's programming skills, experience level, and interests.",
    backstory="Experienced developer mentor who creates developer profiles.",
    llm=llm,
    verbose=True
)


issue_recommender = Agent(
    role="Issue Recommendation Expert",
    goal="Recommend beginner friendly GitHub issues.",
    backstory="Experienced open source contributor who finds good first issues.",
    llm=llm,
    verbose=True
)


roadmap_creator = Agent(
    role="Contribution Roadmap Creator",
    goal="Create a step-by-step open source contribution roadmap.",
    backstory="Open source mentor helping developers make successful contributions.",
    llm=llm,
    verbose=True
)


checklist_creator = Agent(
    role="Contribution Checklist Creator",
    goal="Generate checklist before submitting a pull request.",
    backstory="Experienced GitHub reviewer ensuring contribution quality.",
    llm=llm,
    verbose=True
)