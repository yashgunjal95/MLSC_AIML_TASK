"""
Simple RAG Implementation with Google Gemini
For testing and demonstration purposes
"""

import os
from dotenv import load_dotenv
import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import google.generativeai as genai

load_dotenv()

class SimpleGeminiRAG:
    def __init__(self, gemini_api_key=None):
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize Gemini - try multiple env variable names and model names
        api_key = gemini_api_key or os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        
        if api_key:
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
            
            self.gemini_model = None
            for model_name in model_names:
                try:
                    test_model = genai.GenerativeModel(model_name)
                    # Test the model with a simple request
                    test_response = test_model.generate_content("Hello")
                    self.gemini_model = test_model
                    print(f"✅ Successfully using model: {model_name}")
                    break
                except Exception as e:
                    print(f"❌ Model {model_name} failed: {str(e)}")
                    continue
            
            if not self.gemini_model:
                print("❌ No working Gemini model found!")
        else:
            print("❌ No Gemini API key found in environment variables!")
            self.gemini_model = None
        
        self.chunks = []
        self.embeddings = None
        self.index = None
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF: {e}")
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
    
    def create_embeddings(self, text):
        """Process text and create embeddings"""
        # Split into chunks
        self.chunks = self.chunk_text(text)
        print(f"Created {len(self.chunks)} chunks")
        
        # Create embeddings
        self.embeddings = self.embedding_model.encode(self.chunks)
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings.astype('float32'))
        
        print("Embeddings created and indexed successfully!")
    
    def retrieve_relevant_chunks(self, question, k=3):
        """Retrieve most relevant chunks for a question"""
        if self.index is None:
            return []
        
        # Embed the question
        question_embedding = self.embedding_model.encode([question])
        
        # Search for similar chunks
        distances, indices = self.index.search(question_embedding.astype('float32'), k)
        
        # Return relevant chunks
        relevant_chunks = [self.chunks[i] for i in indices[0]]
        return relevant_chunks
    
    def generate_answer(self, question, context_chunks):
        """Generate answer using Gemini"""
        if not self.gemini_model:
            return "Gemini model not initialized. Please provide API key."
        
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
            return f"Error generating answer: {e}"
    
    def ask_question(self, question):
        """Main method to ask a question and get an answer"""
        if self.index is None:
            return "Please process a document first."
        
        # Retrieve relevant chunks
        relevant_chunks = self.retrieve_relevant_chunks(question)
        
        if not relevant_chunks:
            return "No relevant information found."
        
        # Generate answer
        answer = self.generate_answer(question, relevant_chunks)
        return answer

def demo():
    """Demo function to test the RAG system"""
    print("🤖 Simple RAG Demo with Google Gemini")
    print("=" * 50)
    
    # Load API key from .env
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ No API key found in .env file!")
        print("💡 Make sure you have GEMINI_API_KEY in your .env file")
        return
    
    print(f"✅ API key loaded from .env: {api_key[:10]}...{api_key[-4:]}")
    
    # Initialize RAG system
    rag = SimpleGeminiRAG(gemini_api_key=api_key)
    
    if not rag.gemini_model:
        print("Failed to initialize Gemini! Please check your API key.")
        return
    
    # Get PDF path
    pdf_path = input("Enter path to your PDF file: ").strip()
    
    if not os.path.exists(pdf_path):
        print("PDF file not found!")
        return
    
    # Process PDF
    print("\nProcessing PDF...")
    text = rag.extract_text_from_pdf(pdf_path)
    
    if not text:
        print("Failed to extract text from PDF!")
        return
    
    print(f"Extracted {len(text)} characters from PDF")
    
    # Create embeddings
    print("Creating embeddings...")
    rag.create_embeddings(text)
    
    # Interactive Q&A
    print("\n🎯 You can now ask questions! (type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        question = input("\nYour question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        if not question:
            continue
        
        print("\nGemini is thinking...")
        answer = rag.ask_question(question)
        print(f"\n🤖 Gemini's Answer: {answer}")

def test_with_sample_text():
    """Test RAG with sample text instead of PDF"""
    
    # Sample document text
    sample_text = """
    Machine Learning and Artificial Intelligence
    
    Machine Learning (ML) is a subset of artificial intelligence that focuses on the development of algorithms 
    and statistical models that enable computer systems to improve their performance on a specific task through experience.
    
    Deep Learning is a subset of machine learning that uses neural networks with multiple layers to model and understand 
    complex patterns in data. It has been particularly successful in areas like image recognition, natural language 
    processing, and speech recognition.
    
    Natural Language Processing (NLP) is a field of AI that focuses on the interaction between computers and humans 
    through natural language. The ultimate objective of NLP is to read, decipher, understand, and make sense of 
    human languages in a manner that is valuable.
    
    Computer Vision is a field of AI that trains computers to interpret and understand the visual world. Using digital 
    images from cameras and videos and deep learning models, machines can accurately identify and classify objects.
    
    The applications of AI include healthcare, finance, transportation, entertainment, and many other industries. 
    AI is transforming how we work, live, and interact with technology.
    """
    
    print("🧪 Testing RAG System with Sample Text and Gemini")
    print("=" * 60)
    
    # Load API key from .env
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ No API key found in .env file!")
        print("💡 Make sure you have GEMINI_API_KEY in your .env file")
        return
    
    print(f"✅ API key loaded from .env: {api_key[:10]}...{api_key[-4:]}")
    
    # Initialize RAG
    rag = SimpleGeminiRAG(gemini_api_key=api_key)
    
    if not rag.gemini_model:
        print("Failed to initialize Gemini! Please check your API key.")
        return
    
    # Process sample text
    print("Processing sample text...")
    rag.create_embeddings(sample_text)
    
    # Test questions
    test_questions = [
        "What is machine learning?",
        "What are the applications of AI?",
        "How is deep learning different from machine learning?",
        "What is computer vision?",
        "What does NLP stand for?"
    ]
    
    print("\n🎯 Testing with sample questions:")
    print("-" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        answer = rag.ask_question(question)
        print(f"   Gemini's Answer: {answer}")
    
    print("\n✅ Test completed! Your RAG system with Gemini is working.")
    print("\nNow you can:")
    print("1. Run 'streamlit run rag_app_gemini.py' for the web interface")
    print("2. Run 'python simple_rag_gemini.py' for command line version")
    print("3. Upload your own PDF documents to test with real content")

if __name__ == "__main__":
    choice = input("Choose: (1) Test with sample text (2) Test with PDF: ").strip()
    
    if choice == "1":
        test_with_sample_text()
    else:
        demo()