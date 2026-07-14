from crewai import Task
from crew.agents import (
    repository_recommender,
    repository_explainer,
    skill_analyzer,
    issue_recommender,
    roadmap_creator,
    checklist_creator
)

skill_task = Task(
    description="""
Analyze the user's programming skills, experience level, and interests.
Create a structured developer profile.
""",
    expected_output="A structured developer profile.",
    agent=skill_analyzer
)

repository_task = Task(
    description="""
Recommend suitable GitHub repositories based on the user's profile.
""",
    expected_output="Top GitHub repository recommendations.",
    agent=repository_recommender
)

explanation_task = Task(
    description="""
Explain the selected GitHub repository in beginner-friendly language.
""",
    expected_output="Repository explanation.",
    agent=repository_explainer
)

issue_task = Task(
    description="""
Recommend beginner-friendly GitHub issues from the repository.
""",
    expected_output="List of beginner-friendly issues.",
    agent=issue_recommender
)

roadmap_task = Task(
    description="""
Create a step-by-step contribution roadmap.
""",
    expected_output="Contribution roadmap.",
    agent=roadmap_creator
)

checklist_task = Task(
    description="""
Generate a pull request preparation checklist.
""",
    expected_output="Contribution checklist.",
    agent=checklist_creator
)