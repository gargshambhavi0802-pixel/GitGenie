# GitGenie

### AI-Powered Open Source Contribution Assistant

GitGenie is an AI-based assistant that helps beginners understand GitHub repositories and make meaningful open-source contributions.

It uses AI agents to analyze repositories, explain projects, recommend repositories, and create contribution roadmaps based on real GitHub data.

---

## 🚀 Features

### 1. Repository Explainer Agent

Helps beginners understand any GitHub repository.

It provides:

* Repository overview
* Tech stack information
* Important files explanation
* Beginner entry points
* Project understanding guidance

---

### 2. Contribution Roadmap Agent

Creates a practical contribution plan for a specific repository.

It provides:

* Repository setup steps
* Beginner contribution suggestions
* Intermediate and advanced contribution ideas
* Suitable GitHub issues
* Required skills
* Contribution workflow
* 30-day contribution plan

---

### 3. Repository Recommendation Agent

Helps users discover suitable open-source repositories based on their interests and skills.

It analyzes:

* Repository popularity
* Programming language
* Difficulty level
* Beginner friendliness

---

### 4. Skill Analysis Agent

Helps users understand the skills required for contributing to open-source projects.

It recommends:

* Technologies to learn
* Required tools
* Learning direction

---

## 🏗️ Project Architecture

```
GitGenie
│
├── repository_explainer_agent.py
├── contribution_roadmap_agent.py
├── repository_recommendation_agent.py
├── skill_agent.py
│
├── .env
└── README.md
```

---

## 🛠️ Tech Stack

* Python
* Google Gemini API
* Groq API (Fallback LLM)
* GitHub REST API
* OpenAI SDK compatible clients
* python-dotenv
* Requests

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/siddhigrg1201/GitGenie.git
```

Move into the project folder:

```bash
cd GitGenie
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Usage

### Repository Explainer

```bash
python repository_explainer_agent.py
```

Enter repository:

```
owner/repository
```

Example:

```
tiangolo/fastapi
```

---

### Contribution Roadmap

```bash
python contribution_roadmap_agent.py
```

Example:

```
langchain-ai/langchain
```

---

## 🔄 AI Model Fallback System

GitGenie uses a fallback mechanism:

```
User Request
      |
      ↓
Gemini API
      |
      ↓
If unavailable
      |
      ↓
Groq API
```

This ensures responses can still be generated even when the primary AI provider reaches its limit.

---

## 🎯 Future Improvements

* Web-based UI using Streamlit
* GitHub authentication
* Pull Request analysis agent
* Issue difficulty prediction
* Personalized contribution recommendations
* Multi-agent workflow using LangGraph

---

## 👩‍💻Contributors

**Siddhi Garg**

**Shambhavi Garg**

**Shivangi Gupta**

**Shruti Kumari**


GitHub:
https://github.com/siddhigrg1201

