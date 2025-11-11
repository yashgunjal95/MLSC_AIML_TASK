"""CodeSense AI - Main Streamlit Application"""

import streamlit as st
from src.core.code_parser import CodeParser
from src.core.vector_store import VectorStore
from src.rag.retriever import CodeRetriever
from src.llm.ollama_client import OllamaClient
from src.agents.router import RouterAgent
from src.utils.file_handler import (
    get_file_language,
    read_file,
    save_uploaded_file
)
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Page config
st.set_page_config(
    page_title="CodeSense AI",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = VectorStore()

if "llm_client" not in st.session_state:
    st.session_state.llm_client = OllamaClient()

if "router" not in st.session_state:
    retriever = CodeRetriever(st.session_state.vector_store)
    st.session_state.router = RouterAgent(st.session_state.llm_client, retriever)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "indexed" not in st.session_state:
    st.session_state.indexed = False

# Title
st.title("🤖 CodeSense AI")
st.caption("Advanced Code Intelligence System with RAG")

# Sidebar - File Upload
with st.sidebar:
    st.header("📁 Upload Code")
    
    # Check Ollama status
    if st.session_state.llm_client.check_model():
        st.success("✅ Ollama connected")
    else:
        st.error("❌ Ollama not available. Please start Ollama and pull codellama:7b")
    
    uploaded_files = st.file_uploader(
        "Upload code files",
        accept_multiple_files=True,
        type=["py", "js", "jsx", "ts", "tsx", "json", "md"]
    )
    
    if uploaded_files and st.button("📊 Index Files"):
        with st.spinner("Indexing files..."):
            parser = CodeParser()
            all_chunks = []
            
            for uploaded_file in uploaded_files:
                # Save file
                file_path = save_uploaded_file(uploaded_file)
                st.session_state.uploaded_files.append(file_path)
                
                # Parse file
                content = read_file(file_path)
                language = get_file_language(file_path)
                chunks = parser.parse_file(file_path, content, language)
                all_chunks.extend(chunks)
                
                st.success(f"✓ {uploaded_file.name} ({len(chunks)} chunks)")
            
            # Add to vector store
            st.session_state.vector_store.add_chunks(all_chunks)
            st.session_state.indexed = True
            st.success(f"🎉 Indexed {len(all_chunks)} total chunks!")
    
    # Stats
    if st.session_state.indexed:
        st.divider()
        stats = st.session_state.vector_store.get_stats()
        st.metric("Total Chunks", stats["total_chunks"])
        st.metric("Files Uploaded", len(st.session_state.uploaded_files))
    
    # Clear button
    if st.button("🗑️ Clear All"):
        st.session_state.vector_store.clear()
        st.session_state.chat_history = []
        st.session_state.uploaded_files = []
        st.session_state.indexed = False
        st.rerun()

# Main area - Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🛡️ Review", "🐛 Debug", "📖 Explain"])

with tab1:
    st.subheader("💬 Chat with Your Code")
    mode = "analyzer"

with tab2:
    st.subheader("🛡️ Code Review")
    mode = "reviewer"

with tab3:
    st.subheader("🐛 Debug Assistance")
    mode = "debugger"

with tab4:
    st.subheader("📖 Code Explanation")
    mode = "explainer"

# Chat interface (common for all tabs)
if not st.session_state.indexed:
    st.info("👆 Please upload and index your code files to get started!")
else:
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about your code..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Route and process
            agent = st.session_state.router.route_query(prompt, mode=mode)
            
            for token in agent.process_query(
                prompt, 
                st.session_state.chat_history[:-1],  # Exclude current query
                stream=True
            ):
                full_response += token
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        # Add assistant message
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

# Footer
st.divider()
st.caption("Built with ❤️ for MLSC Internal Challenge | Advanced RAG + Pro LangChain")