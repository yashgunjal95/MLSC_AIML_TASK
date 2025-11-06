import streamlit as st
import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import tempfile

class OfflineRAGBot:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunks = []
        self.embeddings = None
        self.index = None
        
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
            
            # Return relevant chunks with scores
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                results.append({
                    'chunk': self.chunks[idx],
                    'score': float(distance),
                    'rank': i + 1
                })
            
            return results
        except Exception as e:
            st.error(f"Error retrieving chunks: {str(e)}")
            return []
    
    def generate_simple_answer(self, question, context_chunks):
        """Generate a simple answer based on retrieved chunks"""
        if not context_chunks:
            return "No relevant information found in the document."
        
        # Combine the most relevant chunks
        combined_text = "\n\n".join([chunk['chunk'] for chunk in context_chunks])
        
        # Simple keyword-based response
        question_lower = question.lower()
        
        # Create a basic response
        response = f"Based on the document content, here are the most relevant sections for your question '{question}':\n\n"
        
        for i, chunk_data in enumerate(context_chunks, 1):
            chunk = chunk_data['chunk']
            score = chunk_data['score']
            
            # Truncate long chunks for display
            display_chunk = chunk[:500] + "..." if len(chunk) > 500 else chunk
            
            response += f"**Relevant Section {i}** (Similarity Score: {score:.2f}):\n"
            response += f"{display_chunk}\n\n"
        
        # Add a simple summary attempt
        if any(word in question_lower for word in ['what is', 'define', 'definition']):
            response += "**Summary**: The document appears to discuss the topics mentioned above. "
        elif any(word in question_lower for word in ['how', 'process', 'steps']):
            response += "**Process/Steps**: The relevant sections above contain procedural information. "
        elif any(word in question_lower for word in ['why', 'reason', 'because']):
            response += "**Reasoning**: The document provides explanations in the sections above. "
        
        response += "Please review the relevant sections for detailed information."
        
        return response

def main():
    st.set_page_config(
        page_title="Offline RAG PDF Bot - MLSC Challenge",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Offline RAG PDF Bot")
    st.markdown("### MLSC AI/ML Challenge - Advanced Level")
    st.markdown("Upload a PDF and get relevant sections for your questions - **No API key needed!**")
    
    # Initialize session state
    if 'rag_bot' not in st.session_state:
        st.session_state.rag_bot = OfflineRAGBot()
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False
    
    # Sidebar for setup
    with st.sidebar:
        st.header("🔧 Setup")
        
        st.success("✅ No API key needed!")
        st.info("This version works completely offline using semantic search to find relevant document sections.")
        
        # PDF upload
        uploaded_file = st.file_uploader(
            "Upload PDF", 
            type="pdf",
            help="Upload a PDF document to search through"
        )
        
        if uploaded_file:
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
        if st.session_state.pdf_processed:
            st.success("✅ PDF Processed")
        else:
            st.warning("⏳ Need PDF Upload")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Search Document")
        
        if st.session_state.pdf_processed:
            # Question input
            question = st.text_input(
                "Your Question:",
                placeholder="What is this document about?"
            )
            
            if st.button("🔍 Search", type="primary") and question:
                with st.spinner("Searching document..."):
                    results = st.session_state.rag_bot.retrieve_relevant_chunks(question)
                    answer = st.session_state.rag_bot.generate_simple_answer(question, results)
                    
                    st.markdown("### 📄 Search Results:")
                    st.write(answer)
            
            # Sample questions
            st.markdown("### 📝 Try These Sample Questions:")
            sample_questions = [
                "What is the main topic of this document?",
                "Can you find information about key concepts?",
                "What are the important points mentioned?",
                "Who are the main people discussed?",
                "What conclusions are drawn?"
            ]
            
            for i, sample_q in enumerate(sample_questions):
                if st.button(f"💡 {sample_q}", key=f"sample_{i}"):
                    with st.spinner("Searching document..."):
                        results = st.session_state.rag_bot.retrieve_relevant_chunks(sample_q)
                        answer = st.session_state.rag_bot.generate_simple_answer(sample_q, results)
                        st.markdown("### 📄 Search Results:")
                        st.write(answer)
        else:
            st.info("👈 Please upload and process a PDF document to get started.")
    
    with col2:
        st.header("ℹ️ How it Works")
        st.markdown("""
        **Offline RAG Process:**
        
        1. **📄 PDF Upload**: Extract text from your document
        
        2. **✂️ Text Chunking**: Split into manageable pieces
        
        3. **🔢 Embeddings**: Convert text to vectors using sentence transformers
        
        4. **💾 Vector Store**: Store in FAISS for fast search
        
        5. **🔍 Semantic Search**: Find relevant chunks for your question
        
        6. **📋 Results**: Display most relevant sections
        """)
        
        st.markdown("### 🆓 Offline Benefits")
        st.markdown("""
        - **No API needed** - Works completely offline
        - **Fast search** - Instant semantic similarity
        - **Privacy** - Your documents stay local
        - **Free** - No usage costs
        - **Reliable** - No network dependencies
        """)
        
        if st.session_state.pdf_processed:
            st.markdown("---")
            st.markdown("**Document Stats:**")
            st.write(f"📊 Chunks: {len(st.session_state.rag_bot.chunks)}")
            st.write(f"🔢 Embeddings: {st.session_state.rag_bot.embeddings.shape if st.session_state.rag_bot.embeddings is not None else 'None'}")

if __name__ == "__main__":
    main()