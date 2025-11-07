# PDF ChatBot (RAG)

This is a cli-based simple Python bot that uses RAG (Retrieval-Augmented Generation) to answer questions about a PDF document as Voice  output.

It uses a `sentence-transformer` to find relevant parts of the PDF and `google/flan-t5-small` to generate answers.

## Features
* Loads and processes a local PDF file.
* Answers questions based *only* on the PDF's content.
* Speaks the answer out loud using Google Text-to-Speech (gTTS).

## How to Install

1.  **Clone this repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Create a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the packages:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  Place your PDF file in the 'pdfs' folder and update the config.
2.  Run the bot:
    ```bash
    python RAGbot.py
    ```

3.  Wait for the model to load and the PDF to be processed.
4.  Type your question and press Enter.
5.  Type `exit` to quit.