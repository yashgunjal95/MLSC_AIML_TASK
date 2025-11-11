# RAG Q&A System with Google Gemini

This is a Retrieval-Augmented Generation (RAG) system that allows you to ask questions about PDF documents and websites using Google Gemini AI.

## Features
- Ingest PDF files and websites into a vector database (FAISS)
- Semantic search through your documents
- Ask questions and get AI-powered answers using Google Gemini
- Streamlit web interface for easy interaction

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Gemini API key:
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file in this directory with:
```
GEMINI_API_KEY=your_api_key_here
```

3. Ingest your documents:
```bash
# Put PDF files in the data/ folder, then run:
python ingest.py --data_folder data

# Or ingest from a URL:
python ingest.py --url https://example.com/document
```

4. Run the Streamlit app:
```bash
streamlit run app_streamlit.py
```

## API Migration Notes

This project was converted from OpenAI to Google Gemini API:
- Replaced `openai` dependency with `google-generativeai`
- Changed API calls from OpenAI ChatCompletion to Gemini GenerativeModel
- Updated environment variable from `OPENAI_API_KEY` to `GEMINI_API_KEY`
- All retrieval and embedding logic remains unchanged (using Sentence Transformers)

## Files
- `app_streamlit.py` - Main Streamlit web application
- `ingest.py` - Script to process and index documents
- `utils.py` - Utility functions for text processing
- `requirements.txt` - Python dependencies