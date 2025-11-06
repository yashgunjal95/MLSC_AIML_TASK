import streamlit as st
import os
from dotenv import load_dotenv
import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import google.generativeai as genai
import tempfile

# Load environment variables
load_dotenv()

class GeminiRAGBot:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunks = []
        self.embeddings = None
        self.index = None
        self.gemini_model = None
        
    def setup_gemini(self, api_key=None):
        """Setup Gemini client"""
        # Use provided key or load from environment
        api_key = api_key or os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            st.error("No Gemini API key found!")
            return False
        
        try:
            genai.configure(api_key=api_key)
            
            # Try different model names until one works (updated with working models)
            model_names = [
                'models/gemini-2.5-flash-preview-05-20',
                'models/gemini-2.5-flash',
                'models/gemini-2.0-flash',
                'models/gemini-flash-latest',
                'models/gemini-2.5-flash-lite',
                'models/gemini-2.0-flash-lite'
            ]
            
            for model_name in model_names:
                try:
                    test_model = genai.GenerativeModel(model_name)
                    # Test the model
                    test_response = test_model.generate_content("Hello")
                    self.gemini_model = test_model
                    st.success(f"✅ Using model: {model_name}")
                    return True
                except Exception as e:
                    st.warning(f"Model {model_name} failed: {str(e)}")
                    continue
            
            st.error("No working Gemini model found!")
            return False
            
        except Exception as e:
            st.error(f"Error setting up Gemini: {str(e)}")
            return False
        
    def extract_text_from_pdf(self, pdf_file):
        """Extract text from uploaded PDF file"""
        text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return None
        return text
    
    def chunk_text(self, text, chunk_size=1000, overlap=200):
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
            
        return chunks
    
    def process_document(self, text):
        """Split text into chunks and create embeddings"""
        if not text:
            return False
            
        try:
            # Split text into chunks
            self.chunks = self.chunk_text(text)
            
            # Create embeddings
            self.embeddings = self.embedding_model.encode(self.chunks)
            
            # Create FAISS index
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(self.embeddings.astype('float32'))
            
            return True
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")
            return False
    
    def retrieve_relevant_chunks(self, question, k=3):
        """Retrieve most relevant chunks for a question"""
        if self.index is None:
            return []
        
        try:
            # Embed the question
            question_embedding = self.embedding_model.encode([question])
            
            # Search for similar chunks
            distances, indices = self.index.search(question_embedding.astype('float32'), k)
            
            # Return relevant chunks
            relevant_chunks = [self.chunks[i] for i in indices[0]]
            return relevant_chunks
        except Exception as e:
            st.error(f"Error retrieving chunks: {str(e)}")
            return []
    
    def generate_answer(self, question, context_chunks):
        """Generate answer using Gemini"""
        if not self.gemini_model:
            return "Gemini model not initialized."
        
        # Combine context chunks
        context = "\n\n".join(context_chunks)
        
        # Create prompt
        prompt = f"""Based on the following context from a document, answer the question. If the answer is not in the context, say "I don't have enough information to answer that question based on the provided document."

Context:
{context}

Question: {question}

Please provide a clear and concise answer based only on the information in the context above."""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def ask_question(self, question):
        """Main method to ask a question and get an answer"""
        if self.index is None:
            return "Please upload and process a PDF first."
        
        # Retrieve relevant chunks
        relevant_chunks = self.retrieve_relevant_chunks(question)
        
        if not relevant_chunks:
            return "No relevant information found."
        
        # Generate answer
        answer = self.generate_answer(question, relevant_chunks)
        return answer

def main():
    st.set_page_config(
        page_title="RAG PDF Bot with Gemini - MLSC Challenge",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 RAG PDF Bot with Google Gemini")
    st.markdown("### MLSC AI/ML Challenge - Advanced Level")
    st.markdown("Upload a PDF and ask questions about its content using Google's free Gemini API!")
    
    # Initialize session state
    if 'rag_bot' not in st.session_state:
        st.session_state.rag_bot = GeminiRAGBot()
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False
    if 'gemini_ready' not in st.session_state:
        st.session_state.gemini_ready = False
    
    # Sidebar for setup
    with st.sidebar:
        st.header("🔧 Setup")
        
        # Auto-load API key from .env or allow manual input
        env_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        
        if env_key and not st.session_state.gemini_ready:
            st.info("🔑 API key found in .env file")
            if st.button("🔗 Connect with .env API Key"):
                with st.spinner("Connecting to Gemini..."):
                    if st.session_state.rag_bot.setup_gemini():
                        st.session_state.gemini_ready = True
                        st.rerun()
        
        # Manual API key input (fallback)
        st.markdown("**Or enter API key manually:**")
        gemini_key = st.text_input(
            "Gemini API Key", 
            type="password",
            help="Get your FREE API key from Google AI Studio",
            placeholder="Leave empty to use .env file"
        )
        
        if gemini_key and not st.session_state.gemini_ready:
            if st.button("🔗 Connect to Gemini"):
                with st.spinner("Connecting to Gemini..."):
                    if st.session_state.rag_bot.setup_gemini(gemini_key):
                        st.session_state.gemini_ready = True
                        st.rerun()
        
        # Instructions for getting API key
        with st.expander("📋 How to get Gemini API key"):
            st.markdown("1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)")
            st.markdown("2. Click 'Create API Key'")
            st.markdown("3. Copy the key and add it to .env file or paste above")
        
        # PDF upload
        uploaded_file = st.file_uploader(
            "Upload PDF", 
            type="pdf",
            help="Upload a PDF document to ask questions about"
        )
        
        if uploaded_file and st.session_state.gemini_ready:
            if st.button("🔄 Process PDF"):
                with st.spinner("Processing PDF..."):
                    # Extract text
                    text = st.session_state.rag_bot.extract_text_from_pdf(uploaded_file)
                    
                    if text:
                        # Process document
                        if st.session_state.rag_bot.process_document(text):
                            st.session_state.pdf_processed = True
                            st.success(f"✅ PDF processed! Created {len(st.session_state.rag_bot.chunks)} chunks.")
                        else:
                            st.error("❌ Failed to process document.")
                    else:
                        st.error("❌ Failed to extract text from PDF.")
        
        # Status indicators
        st.markdown("---")
        st.markdown("**Status:**")
        if st.session_state.gemini_ready:
            st.success("✅ Gemini Ready")
        else:
            st.warning("⏳ Need Gemini API Key")
            
        if st.session_state.pdf_processed:
            st.success("✅ PDF Processed")
        else:
            st.warning("⏳ Need PDF Upload")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Ask Questions")
        
        if st.session_state.pdf_processed and st.session_state.gemini_ready:
            # Question input
            question = st.text_input(
                "Your Question:",
                placeholder="What is this document about?"
            )
            
            if st.button("🔍 Get Answer", type="primary") and question:
                with st.spinner("Gemini is thinking..."):
                    answer = st.session_state.rag_bot.ask_question(question)
                    
                    st.markdown("### 🤖 Gemini's Answer:")
                    st.write(answer)
            
            # Sample questions
            st.markdown("### 📝 Try These Sample Questions:")
            sample_questions = [
                "What is the main topic of this document?",
                "Can you summarize the key points?",
                "What are the important dates mentioned?",
                "Who are the main people discussed?",
                "What conclusions does the document reach?"
            ]
            
            for i, sample_q in enumerate(sample_questions):
                if st.button(f"💡 {sample_q}", key=f"sample_{i}"):
                    with st.spinner("Gemini is thinking..."):
                        answer = st.session_state.rag_bot.ask_question(sample_q)
                        st.markdown("### 🤖 Gemini's Answer:")
                        st.write(answer)
        else:
            st.info("👈 Please complete the setup in the sidebar to get started:")
            if not st.session_state.gemini_ready:
                st.write("1. ⚠️ Get and enter your FREE Gemini API key")
            if not st.session_state.pdf_processed:
                st.write("2. ⚠️ Upload and process a PDF document")
    
    with col2:
        st.header("ℹ️ How it Works")
        st.markdown("""
        **RAG with Gemini Process:**
        
        1. **📄 PDF Upload**: Extract text from your document
        
        2. **✂️ Text Chunking**: Split into manageable pieces
        
        3. **🔢 Embeddings**: Convert text to vectors using sentence transformers
        
        4. **💾 Vector Store**: Store in FAISS for fast search
        
        5. **🔍 Retrieval**: Find relevant chunks for your question
        
        6. **🤖 Generation**: Google Gemini creates contextual answers
        """)
        
        st.markdown("### 🆓 Why Gemini?")
        st.markdown("""
        - **Completely FREE** to use
        - **No credit card** required
        - **High quality** responses
        - **Fast** generation
        - **Easy setup** with Google account
        """)
        
        if st.session_state.pdf_processed:
            st.markdown("---")
            st.markdown("**Document Stats:**")
            st.write(f"📊 Chunks: {len(st.session_state.rag_bot.chunks)}")
            st.write(f"🔢 Embeddings: {st.session_state.rag_bot.embeddings.shape if st.session_state.rag_bot.embeddings is not None else 'None'}")

if __name__ == "__main__":
    main()