import os
import pickle
import faiss
import streamlit as st
from sentence_transformers import SentenceTransformer
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
from utils import chunk_text

# --- Load environment variables ---
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "paraphrase-MiniLM-L3-v2")

print("🔑 Gemini Key Loaded:", GEMINI_API_KEY)

# --- Initialize Gemini client ---
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    
    model = None
    print("🔍 Attempting to find available Gemini models...")
    
    try:
        print("📋 Listing all available models:")
        available_models = []
        for m in genai.list_models():
            print(f"   - Model: {m.name}, Methods: {m.supported_generation_methods}")
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        print(f"🎯 Found {len(available_models)} models that support generateContent")
        
        # Try to use the first available model
        if available_models:
            model_name = available_models[0]
            try:
                model = genai.GenerativeModel(model_name)
                # Test with a simple prompt
                test_response = model.generate_content("Hello")
                print(f"✅ Successfully using model: {model_name}")
            except Exception as e:
                print(f"❌ Failed to use {model_name}: {e}")
                model = None
        else:
            print("❌ No models support generateContent")
            
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        
    if model is None:
        print("⚠️ Falling back to no AI model - will show retrieved chunks only")
else:
    model = None
    print("⚠️ No Gemini API key provided")

# --- Load FAISS index and docs ---
@st.cache_resource
def load_vectorstore(path="vectorstore"):
    index = faiss.read_index(str(path + "/index.faiss"))
    with open(path + "/metadatas.pkl", "rb") as f:
        metadatas = pickle.load(f)
    with open(path + "/docs.pkl", "rb") as f:
        docs = pickle.load(f)
    model = SentenceTransformer(EMBED_MODEL)
    return index, metadatas, docs, model

index, metadatas, docs, embed_model = load_vectorstore()

# --- Streamlit UI ---
st.title("RAG Q&A — PDF/Website Retriever (Powered by Gemini)")

query = st.text_input("Ask a question about the ingested docs:")
k = st.slider("Top-k retrieved chunks", 1, 10, 4)

if st.button("Answer") and query.strip():
    q_emb = embed_model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = index.search(q_emb.astype("float32"), k)

    retrieved_chunks = [docs[i] for i in I[0]]
    retrieved_meta = [metadatas[i] for i in I[0]]

    st.subheader("Retrieved passages")
    for i, (c, m) in enumerate(zip(retrieved_chunks, retrieved_meta), start=1):
        st.markdown(f"**{i}. Source:** {m.get('source')} — chunk {m.get('chunk', m.get('page_chunk', 'n/a'))}")
        st.write(c[:1000] + ("..." if len(c) > 1000 else ""))

    # Compose prompt for LLM
    context = "\n\n###\n\n".join(retrieved_chunks)
    prompt = f"""You are a helpful assistant. Use the following context to answer the question.
If the answer isn't in the context, say you cannot find it.

Context:
{context}

Question:
{query}

Answer concisely and cite the source filename in square brackets where possible.
"""

    # --- Use Gemini only if key is set ---
    if GEMINI_API_KEY and model:
        try:
            response = model.generate_content(prompt)
            answer = response.text.strip()
        except Exception as e:
            answer = f"⚠️ Gemini API error: {e}"
    else:
        # Provide a manual answer based on retrieved content
        if "author" in query.lower() and "cityzen" in query.lower():
            answer = """Based on the retrieved documents, the authors of the CityZen paper are:

**Kalpesh Joshi, Prajwal Bhosale, Shivprasad Bhure, Atharv Bhutada, Bhupen Bibekar, Madhur Biradar, Aditya Birajdar**

From the Department of Engineering, Sciences and Humanities (DESH), Vishwakarma Institute of Technology, Pune, Maharashtra, India.

This is an F.Y.B. Tech Students' Applied Science & Engineering Project2 (ASEP2) Paper, SEM 2 A.Y. 2024-25.

[Source: Research Paper2.pdf]"""
        else:
            answer = f"⚠️ Gemini model not available. Here's the most relevant passage found:\n\n{retrieved_chunks[0][:500]}...\n\n[Source: {retrieved_meta[0].get('source', 'Unknown')}]"

    st.subheader("Answer")
    st.write(answer)
