# 🎓 Gemma-4 Powered: Interactive Learning & Practice Assistant

An AI-powered learning assistant built with **Streamlit** and **Google Gemma** that helps students understand study material, practice concepts, learn through personalized teaching styles, and clear doubts with an AI tutor.

The application acts as a virtual teaching assistant by analyzing learning resources, creating quizzes, providing study roadmaps, and adapting explanations according to the student's preferred learning style.

---

## ✨ Features

### 📄 Study Material Learning
- Upload PDF-based study material.
- Generate concise summaries of complex topics.
- Get a personalized learning roadmap:
  - Prerequisite topics required before understanding the material.
  - Related concepts for deeper knowledge.
  - Advanced topics for further exploration.

---

### 📝 AI Quiz Generator & Evaluation
- Generate quizzes from:
  - Uploaded PDFs
  - User-provided topics

- Supports multiple question formats:
  - 1-2 word answers
  - Short answers (2-3 lines)
  - Long descriptive answers

- AI evaluates responses and provides:
  - Score out of 10
  - Correct answers
  - Performance feedback

---

### 🎭 Learn With Your Favorite AI Tutor
Personalize your learning experience by choosing any teaching style or persona.

Examples:
- Learn concepts like a professor.
- Understand topics through storytelling.
- Learn from a fictional character style.
- Get explanations with different analogies and approaches.

---

### ✨ AI Doubt Solver
- Ask questions on any topic.
- Receive detailed explanations from an AI tutor.
- Helps students resolve doubts instantly.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI Model:** Google Gemma
- **PDF Processing:** PyPDF
- **Programming Language:** Python
- **Environment Management:** python-dotenv

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Create a .env file in the project directory:
```bash
GEMMA_API_KEY=your_api_key_here
```
### 4. Run the application
```bash
streamlit run app.py
```
