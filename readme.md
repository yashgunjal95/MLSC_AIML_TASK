# Anime Mentor Bot 🗡️🌩️  
### Intermediate Level — MLSC Internal AI/ML Challenge

## 📌 Overview
Anime Mentor Bot is a personality-based AI chatbot inspired by calm anime senseis like Kakashi, Gojo, Itachi, and Tanjiro.  
It generates short, wise, mentor-style responses using the **Gemini 2.5 Flash (Free) model**.

This project belongs to the **Intermediate Level**, where the goal is to experiment with system prompts and create unique personalities.

---

## 🔥 Features
- Custom anime-style mentor personality  
- Runs locally in the terminal  
- Uses **Google Gemini Free API**  
- Fast & lightweight  
- No paid tools needed  

---

## 🧠 How It Works
1. The bot uses a **system prompt** that sets the anime mentor personality.  
2. User asks any question (study, motivation, life advice).  
3. Model responds in calm, sharp anime-style lines.  
4. Terminal interface makes the project simple and easy to run.  

---

## 🛠️ Setup & Installation

### 1️⃣ Install Dependencies

pip install -r requirements.txt


2️⃣ Add Your Gemini API Key

Get your free key from:
https://aistudio.google.com/app/apikey

Set it as an environment variable:

Windows PowerShell
setx GOOGLE_API_KEY "your_api_key_here"


Restart PowerShell after doing this.


🚀 Running the Bot
python anime_mentor_bot.py


You will see:

=== Anime Mentor Bot 🌩️ ===
Speak your thoughts, young warrior...


Ask anything like:

Sensei, how do I stay calm before exams?


🧪 Sample Output
User: How do I stay focused?

Mentor:
"Focus is not force.
It's choosing silence over noise,
and purpose over fear."


Sample Screenshots
<img width="1358" height="550" alt="Screenshot" src="https://github.com/user-attachments/assets/748fac67-9606-44ef-99da-101f89734ed2" /> <img width="1441" height="608" alt="Screenshot" src="https://github.com/user-attachments/assets/8c262cb5-d193-4ea6-a6d1-69863b8d8df2" />

Place your own screenshot as:

sample_output.png


📁 Project Structure
Anime-Mentor-Bot/
│── anime_mentor_bot.py
│── requirements.txt
│── README.md
└── sample_output.png

🏷️ Level

✅ Intermediate
(Custom personality using system prompts)


💙 Credits

Created for MLSC Internal Challenge — AI/ML Domain
By Nilesh Sabale
