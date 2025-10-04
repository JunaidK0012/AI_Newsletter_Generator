# 📰 Multi-Agent AI Newsletter Generator

An autonomous multi-agent system (Researcher, Writer, Editor, Designer) that collaboratively generates AI newsletters — from gathering research to producing a polished HTML newsletter.

---

## 🚀 Overview
This project demonstrates how multiple AI agents can coordinate to complete complex creative tasks. Each agent performs a specialized role — researching recent AI trends, writing summaries, refining tone and coherence, and designing the final layout.

The Streamlit dashboard provides full visibility into the workflow — showing live logs, research sources, and final drafts in HTML format.

---

## 📸 Demo  


---

## 🧠 Agent Roles
| Agent | Role | Description |
|-------|------|-------------|
| **Researcher** | Data Gathering | Searches for trending AI research/news and compiles relevant sources. |
| **Writer** | Draft Creation | Generates newsletter content based on research findings. |
| **Editor** | Content Refinement | Enhances clarity, tone, and structure for readability. |
| **Designer** | HTML Generator | Converts the final text into a formatted HTML newsletter. |

---

## 💻 Features
- Multi-agent collaboration using Langgraph
- Streamlit dashboard for monitoring workflow
- Real-time task execution logs
- Auto-generated newsletter in HTML format
- Displays research files and final output in UI

---
## ⚙️ Installation  

### 1️⃣ Clone the repo  
```bash
git clone https://github.com/your-username/multi-agent-newsletter.git
cd multi-agent-newsletter
```

### 2️⃣ Create virtual environment & install dependencies  
```bash
python -m venv venv
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```
### 3️⃣ Create .env file and store necessary API keys there
```bash
GOOGLE_API_KEY = 'YOUR_GEMINI_API_KEY'
TAVILY_API_KEY = 'YOUR_TAVILY_API_KEY'
NEWS_API_KEY = 'YOUR_NEWS_API_KEY'


LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT='https://api.smith.langchain.com'
LANGCHAIN_API_KEY= 'YOUR_LANGCHAIN_API_KEY'
LANGCHAIN_PROJECT='multi_agent_project'


```
### 4️⃣ Run the Streamlit app  
```bash
streamlit run app.py
```

---

## 📚 Tech Stack  
- **Python**  
- **Langgraph** (agent orchestration , tool integration)  
- **Streamlit** (chat UI)  
- **APIs**: Arxiv, Wikipedia,Youtube, Tavily, News APIs  

---


## 🔮 Future Enhancements

-Add memory and context sharing between agents

-Integrate human-in-the-loop editing

-Improve the dashboard UI

-Add email automation for newsletter delivery