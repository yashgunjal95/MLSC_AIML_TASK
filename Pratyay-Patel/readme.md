# 🤖 RAG PDF Question-Answering Bot with Google Gemini

**MLSC AI/ML Challenge - Advanced Level**

A complete Retrieval-Augmented Generation (RAG) application that intelligently answers questions based on PDF documents using Google's **FREE** Gemini API and advanced vector embeddings.

## ✨ Key Features

- **🔄 Automatic Setup**: API key loads from .env file - no manual entry needed
- **📄 Smart PDF Processing**: Extract and intelligently chunk document text
- **🧠 Semantic Search**: Advanced vector embeddings using sentence transformers
- **⚡ Fast Retrieval**: FAISS vector database for lightning-fast similarity search
- **🤖 AI-Powered Answers**: Google Gemini generates contextual responses
- **🌐 Professional Web Interface**: Clean Streamlit UI perfect for demos
- **💻 Command Line Support**: Alternative CLI interface for testing
- **🆓 Completely FREE**: No API costs - uses Google's free Gemini tier

## 🔬 RAG Pipeline Architecture

Our implementation follows the complete RAG (Retrieval-Augmented Generation) workflow:

1. **📄 Document Ingestion**: PDF text extraction using PyPDF2
2. **✂️ Intelligent Chunking**: Text split into overlapping segments for better context
3. **🔢 Vector Embeddings**: Chunks converted to 384-dimensional vectors using sentence-transformers
4. **💾 Vector Database**: FAISS index stores embeddings for sub-second similarity search
5. **🔍 Semantic Retrieval**: User questions matched against document chunks using cosine similarity
6. **🤖 Answer Generation**: Google Gemini synthesizes responses from retrieved context
7. **📱 User Interface**: Professional Streamlit web app with real-time processing

## ⚡ Quick Setup (2 Minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get FREE Gemini API Key
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Sign in with Google account (no credit card needed!)
- Click "Create API Key" 
- Copy the generated key

### 3. Configure Environment
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key:
GEMINI_API_KEY=your_api_key_here
```

### 4. Test Setup
```bash
python quick_test.py
```

**That's it!** 🎉 Your RAG system is ready to use.

## 🚀 Usage Options

### 🌐 Web Interface (Recommended for Demos)
```bash
streamlit run rag_app.py
```
- **Auto-loads API key** from .env file
- **Drag & drop PDF** upload
- **Real-time processing** with progress indicators
- **Professional UI** perfect for presentations
- **Sample questions** to get started quickly

### 💻 Command Line Interface
```bash
python simple_rag.py
```
- **Batch processing** for multiple documents
- **Direct file path** input
- **Interactive Q&A** session
- **Great for testing** and development

### 🧪 Quick Testing
```bash
# Test with built-in sample data (no PDF needed)
python test_with_sample.py

# Verify API connection
python quick_test.py
```

## � Exxample Questions to Try

**General Understanding:**
- "What is this document about?"
- "Summarize the main points in 3 sentences"
- "What are the key topics discussed?"

**Specific Information:**
- "Who are the main people mentioned?"
- "What dates or deadlines are important?"
- "What are the technical requirements?"

**Analysis & Insights:**
- "What conclusions does the author reach?"
- "What problems does this document address?"
- "What recommendations are made?"

**Perfect for testing with:**
- 📚 Course notes and textbooks
- 📄 Research papers and articles  
- 📋 Technical documentation
- 📊 Reports and presentations

## 🏗️ Technical Architecture

```
📄 PDF Document
    ↓ PyPDF2 Extraction
📝 Raw Text
    ↓ Smart Chunking (1000 chars, 200 overlap)
🧩 Text Chunks
    ↓ sentence-transformers/all-MiniLM-L6-v2
🔢 Vector Embeddings (384-dim)
    ↓ FAISS IndexFlatL2
💾 Vector Database
    ↓ Cosine Similarity Search
🔍 Retrieved Chunks (Top-3)
    ↓ Context + Question
🤖 Google Gemini 2.5 Flash
    ↓ Generated Response
💬 Contextual Answer
```

### 🔧 Core Technologies
- **Frontend**: Streamlit (Professional web interface)
- **PDF Processing**: PyPDF2 (Text extraction)
- **Embeddings**: sentence-transformers (Semantic understanding)
- **Vector DB**: FAISS (Fast similarity search)
- **LLM**: Google Gemini 2.5 Flash (Answer generation)
- **Environment**: python-dotenv (Configuration management)

## � Projedct Structure

```
📁 RAG-PDF-Bot/
├── 🚀 Core Application
│   ├── rag_app.py              # Streamlit web interface
│   ├── simple_rag.py           # CLI + core RAG logic
│   └── requirements.txt        # Dependencies
│
├── 🧪 Testing & Validation  
│   ├── test_with_sample.py     # Built-in sample data test
│   ├── quick_test.py           # API connection verification
│   └── rag_app_offline.py     # Offline fallback version
│
├── ⚙️ Configuration
│   ├── .env                    # Your API key (auto-loaded)
│   └── .env.example           # Template
│
└── 📚 Documentation
    ├── README.md              # This file
    ├── QUICK_START.md         # 2-minute setup guide
    └── GEMINI_SETUP_GUIDE.md  # Detailed setup instructions
```

## 🎓 Technical Skills Demonstrated

### 🤖 AI/ML Concepts
- **Retrieval-Augmented Generation (RAG)**: Complete pipeline implementation
- **Vector Embeddings**: Semantic text representation using transformers
- **Similarity Search**: Efficient nearest neighbor retrieval with FAISS
- **Natural Language Processing**: Text chunking and preprocessing strategies

### 💻 Software Engineering
- **API Integration**: Google Gemini AI service integration
- **Full-Stack Development**: Web interface + backend logic
- **Environment Management**: Secure configuration with .env files
- **Error Handling**: Robust exception handling and user feedback

### 🏗️ System Architecture
- **Modular Design**: Separation of concerns (UI, logic, data)
- **Scalable Storage**: Vector database for large document collections
- **Performance Optimization**: Efficient chunking and retrieval strategies

## 🏆 MLSC Challenge - Advanced Level ✅

### ✅ Requirements Met
- **Complete RAG Implementation**: Full retrieval-augmented generation pipeline
- **Modern AI Integration**: Google Gemini 2.5 Flash model
- **Professional Interface**: Production-ready Streamlit web application
- **Semantic Search**: Advanced vector similarity matching
- **Document Processing**: Intelligent PDF text extraction and chunking

### 🎯 Demo Highlights
- **Zero Setup Friction**: API key auto-loads from environment
- **Real-time Processing**: Live PDF upload and processing
- **Interactive Q&A**: Natural language question answering
- **Professional UI**: Clean interface perfect for presentations
- **Cost-Effective**: Uses completely FREE Google Gemini API

### 🚀 Potential Extensions
- **Multi-format Support**: Word, TXT, HTML document processing
- **Conversation Memory**: Follow-up question context retention
- **Source Attribution**: Highlight exact text sources in responses
- **Batch Processing**: Multiple document analysis
- **Custom Models**: Fine-tuned embeddings for domain-specific content

---

## 🎉 Ready for Submission!

**Built for MLSC AI/ML Challenge 2025**  
*Demonstrating advanced RAG techniques, modern AI integration, and professional software development practices*

### 📞 Quick Support
- **Setup Issues**: Check `GEMINI_SETUP_GUIDE.md`
- **Quick Start**: See `QUICK_START.md` 
- **API Problems**: Run `python quick_test.py`

**Perfect for showcasing cutting-edge AI applications! 🚀**