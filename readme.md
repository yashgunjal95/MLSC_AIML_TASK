🤖 RAG Q&A — PDF / Website Retriever (Gemini-Powered)
📘 Overview

RAG Q&A (Retrieval-Augmented Generation) is a Streamlit-based web application that allows users to upload research papers (PDFs) or retrieve website content, and then ask natural language questions about the ingested documents.

It uses Google Gemini 1.5 Flash as the LLM for generating context-aware answers, combined with a vector-based retriever (FAISS) for document search and relevance ranking.

🚀 Features

📄 Upload and process PDFs or website data

🔍 Ask natural language questions about the uploaded content

⚡ Powered by Google Gemini 1.5 Flash — fast, accurate, and free-tier compatible

🧩 Uses RAG (Retrieval-Augmented Generation) pipeline

🧠 Stores embeddings locally using FAISS

🖥️ Clean Streamlit UI

🧾 Displays source context for transparency

🧠 How It Works

Document Ingestion
Upload PDFs or retrieve text from a website.
The content is split into smaller, meaningful text chunks using LangChain’s RecursiveCharacterTextSplitter.

Embedding Creation
Each text chunk is converted into numerical embeddings using
GoogleGenerativeAIEmbeddings (models/embedding-001).

Question Answering
When the user enters a query:

The retriever finds the top k relevant text chunks using FAISS.

These chunks are sent to Gemini 1.5 Flash as contextual input.

The model generates an accurate, well-formatted answer.

🏗️ Tech Stack
Component	Technology Used
Frontend	Streamlit
Backend	Python
LLM	Google Gemini 1.5 Flash
Vector Database	FAISS
Embeddings	Google Generative AI Embeddings
Document Processing	LangChain
File Handling	PyPDF2
Environment	.env + .gitignore (secure API key handling)
🧩 Folder Structure
📂 prajwal_rag/
├── app_streamlit.py          # Streamlit frontend
├── rag_engine.py             # Core RAG logic
├── requirements.txt          # Dependencies list
├── README.md                 # Documentation
├── .env.example              # Sample environment file (safe)
├── .gitignore                # Ignored files (e.g., .env, .venv)
├── screenshots/              # Output screenshots
│   ├── output1.png
│   └── output2.png
└── vectorstore/              # FAISS vector database

⚙️ Installation & Setup
🪜 Step 1: Clone the Repository
git clone https://github.com/your-username/MLSC_AIML_TASK.git
cd MLSC_AIML_TASK/prajwal_rag

🪜 Step 2: Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

🪜 Step 3: Install Requirements
pip install -r requirements.txt

🪜 Step 4: Add Gemini API Key

Create a .env file in the same directory:

GEMINI_API_KEY=your_google_api_key_here


(Note: .env is ignored by Git for safety)

🪜 Step 5: Run the Streamlit App
streamlit run app_streamlit.py

📸 Screenshots
🖥️ 1. Application Interface

🧠 2. Example Query — “Who are the authors of the CityZen paper?”

🧠 Example Query

User Query:

“Who are the authors of the CityZen research paper?”

Generated Answer:

Based on the retrieved document, the authors of the CityZen paper are:
Kalpesh Joshi, Prajwal Bhosale, Shivprasad Bhure, Atharv Bhutada, Bhupen Bibekar, Madhur Biradar, and Aditya Birajdar.

Source: Research Paper2.pdf (Vishwakarma Institute of Technology, Pune)

🧑‍💻 Contributors
Name	Role
Prajwal Bhosale	Developer & Researcher
Google Gemini 1.5 Flash	LLM Backend
LangChain + Streamlit	Framework & Interface
🏁 Future Enhancements

📚 Multi-file PDF support

🌐 Website content summarization

💬 Persistent chat memory

☁️ Deployment on Streamlit Cloud or Hugging Face Spaces

🪪 License

This project is open-source and distributed under the MIT License
.

💙 Acknowledgment

Built as part of the Microsoft Learn Student Community (MLSC) Internal AI/ML Challenge — “Build Your Own Generative AI App”.

Special thanks to MLSC mentors and organizers for guidance and inspiration. 💫
