"""
Test the RAG system with built-in sample text
No PDF file needed!
"""

import os
from dotenv import load_dotenv
from simple_rag import SimpleGeminiRAG

def test_rag_system():
    print("🧪 Testing RAG System with Sample Text")
    print("=" * 50)
    
    # Sample document about DBMS (relevant to your studies!)
    sample_text = """
    Database Management Systems (DBMS)
    
    A Database Management System (DBMS) is software that enables users to create, manage, and manipulate databases efficiently. 
    It serves as an interface between the database and end users or application programs.
    
    Key Components of DBMS:
    1. Data Definition Language (DDL): Used to define database structure and schema
    2. Data Manipulation Language (DML): Used for inserting, updating, deleting, and retrieving data
    3. Data Control Language (DCL): Used for controlling access to data in the database
    4. Transaction Control Language (TCL): Used for managing transactions in the database
    
    Types of DBMS:
    - Hierarchical DBMS: Data is organized in a tree-like structure
    - Network DBMS: Data is organized in a graph structure
    - Relational DBMS (RDBMS): Data is organized in tables with rows and columns
    - Object-Oriented DBMS: Data is stored as objects
    - NoSQL DBMS: Designed for unstructured data and big data applications
    
    Popular DBMS Examples:
    - MySQL: Open-source relational database
    - PostgreSQL: Advanced open-source relational database
    - Oracle Database: Enterprise-grade commercial database
    - MongoDB: Popular NoSQL document database
    - SQLite: Lightweight embedded database
    
    ACID Properties:
    - Atomicity: Transactions are all-or-nothing
    - Consistency: Database remains in valid state
    - Isolation: Concurrent transactions don't interfere
    - Durability: Committed changes are permanent
    
    Normalization is the process of organizing data to reduce redundancy and improve data integrity.
    The normal forms include 1NF, 2NF, 3NF, and BCNF (Boyce-Codd Normal Form).
    """
    
    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ No API key found in .env file!")
        print("💡 Make sure you have GEMINI_API_KEY in your .env file")
        # Fallback to manual input
        api_key = input("Enter your Gemini API key manually: ").strip()
        if not api_key:
            print("❌ API key is required!")
            return
    else:
        print(f"✅ API key loaded from .env: {api_key[:10]}...{api_key[-4:]}")
    
    # Initialize RAG
    print("🔧 Initializing RAG system...")
    rag = SimpleGeminiRAG(gemini_api_key=api_key)
    
    if not rag.gemini_model:
        print("❌ Failed to initialize Gemini! Please check your API key.")
        return
    
    # Process sample text
    print("📚 Processing DBMS sample text...")
    rag.create_embeddings(sample_text)
    
    # Test questions about DBMS
    test_questions = [
        "What is a DBMS?",
        "What are the ACID properties?",
        "What are the different types of DBMS?",
        "What is normalization?",
        "Give examples of popular databases"
    ]
    
    print("\n🎯 Testing with DBMS questions:")
    print("-" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        answer = rag.ask_question(question)
        print(f"   🤖 Gemini's Answer: {answer}")
    
    print("\n" + "="*50)
    print("✅ Test completed! Your RAG system is working perfectly!")
    print("\n🎯 Next steps:")
    print("1. Run 'streamlit run rag_app_gemini.py' for the web interface")
    print("2. Upload your own PDF files (make sure to use the full file path)")
    print("3. For PDF path, use format: C:\\full\\path\\to\\your\\file.pdf")

if __name__ == "__main__":
    test_rag_system()