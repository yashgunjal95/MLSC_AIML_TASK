# app.py
import os
import time
import json
import requests
import io
import streamlit as st
from openai import OpenAI
from typing import List, Dict

# ----------------------------------------------------------------------
# 1. API KEY SETUP (OpenAI for Text, Clipdrop for Images)
# ----------------------------------------------------------------------
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    CLIPDROP_KEY = st.secrets["CLIPDROP_API_KEY"]
except KeyError as e:
    st.error(f"API key not found in .streamlit/secrets.toml: {e}. Please add it.")
    st.stop()
except Exception as e:
    st.error(f"Error initializing API clients: {e}")
    st.stop()

# ----------------------------------------------------------------------
# NEW: 2. CUSTOM CSS FOR STYLING
# ----------------------------------------------------------------------
# We'll inject CSS to make the idea containers look like "cards"
st.markdown("""
    <style>
    /* Target the st.expander container */
    [data-testid="stExpander"] {
        border: 1px solid #2d2d2d; /* A light border */
        border-radius: 10px;       /* Rounded corners */
        background-color: #0d1117; /* Darker background for the card */
        box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Subtle shadow */
        margin-bottom: 20px;       /* Space between cards */
    }
    
    /* Style the expander header */
    [data-testid="stExpander"] summary {
        font-size: 1.25rem; /* Bigger title */
        font-weight: 600;
        color: #c9d1d9; /* Lighter text color */
    }
    
    /* Style the content inside the expander */
    [data-testid="stExpander"] [data-testid="stVerticalBlock"] {
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 3. STREAMLIT UI CONFIG
# ----------------------------------------------------------------------
st.set_page_config(page_title="IdeaForge 🪄", page_icon="🪄", layout="wide")
st.markdown("<h1 style='text-align:center;'>🪄 IdeaForge — AI Project Idea Generator</h1>", unsafe_allow_html=True)
st.write("Enter your field or combination of domains (e.g., `IoT + AI`, `Healthcare + ML`, `Blockchain`) and get 3 project ideas with title, problem, tools, extensions and a creativity score.")

# Sidebar options
with st.sidebar:
    st.header("Options")
    model_choice = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0)
    
    # NEW: Difficulty Dropdown
    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"], index=1)
    
    temperature = st.slider("Creativity (temperature)", min_value=0.0, max_value=1.2, value=0.9, step=0.1)
    include_images = st.checkbox("Enable Image Generation (Free)", value=True)
    max_tokens = st.slider("Max tokens for response", 300, 3000, 1200, step=100)
    num_ideas = st.slider("Number of ideas to generate", 1, 6, 3)

# Input
domain = st.text_input("Enter domain / field", placeholder="e.g. IoT + AI, Healthcare + ML, FinTech + ML")

col1, col2 = st.columns([1, 1])
with col1:
    generate_btn = st.button("Generate Ideas")
with col2:
    clear_btn = st.button("Clear Results")

# ----------------------------------------------------------------------
# 4. SESSION STATE INITIALIZATION
# ----------------------------------------------------------------------
if "ideas" not in st.session_state:
    st.session_state.ideas = []

if clear_btn:
    st.session_state.ideas = [] 
    st.rerun() 

# ----------------------------------------------------------------------
# 5. HELPER FUNCTIONS
# ----------------------------------------------------------------------

# NEW: Updated prompt to include difficulty
def build_prompt(domain: str, n: int, difficulty: str) -> str:
    return f"""
    You are an expert project mentor for college students. Generate exactly {n} unique project ideas 
    for the domain: "{domain}".
    
    The project complexity MUST be at a "{difficulty}" level.

    Return the output as a valid JSON object.
    The object MUST have a single key "ideas", which holds a list of the {n} idea objects.

    Each idea object in the list must have the fields:
    - title (string)
    - problem_statement (string)
    - tools (list of strings)
    - possible_extension (string)
    - creativity_score (integer 1-10)

    Example output format:
    {{
      "ideas": [
        {{
          "title": "Smart Example",
          "problem_statement": "Short problem explanation...",
          "tools": ["Python", "TensorFlow", "Streamlit"],
          "possible_extension": "Connect to device X",
          "creativity_score": 8
        }}
      ]
    }}
    Do not include any extra commentary. Start the JSON object immediately.
    """

# NEW: Updated function to accept difficulty
def generate_ideas(domain: str, n: int, model_name: str, temperature: float, max_tokens: int, difficulty: str) -> List[Dict]:
    # Pass difficulty to the prompt builder
    prompt = build_prompt(domain, n, difficulty)
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a concise helpful project mentor who outputs only JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        text = response.choices[0].message.content.strip()
        data = json.loads(text)
        return data.get("ideas", []) 

    except json.JSONDecodeError as e:
        st.error("Failed to parse JSON from model response. Retrying might help.")
        st.code(text)
        return []
    except Exception as e:
        if "insufficient_quota" in str(e).lower():
            st.error("OpenAI API request failed: You have exceeded your quota. Please check your billing details.")
        elif "invalid_api_key" in str(e).lower() or "401" in str(e):
             st.error("OpenAI API key is incorrect. Please check your .streamlit/secrets.toml file.")
        else:
            st.error(f"OpenAI API request failed: {e}")
        return []

def generate_image_for_idea(title: str, problem: str) -> bytes:
    url = "https://clipdrop-api.co/text-to-image/v1"
    prompt = f"Conceptual illustration for a project titled: '{title}'. Visualize the core concept or problem: {problem}. Style: minimalist, modern concept art, high-level technical mockup, clean background."
    files = { 'prompt': (None, prompt, 'text/plain') }
    headers = { 'x-api-key': CLIPDROP_KEY }
    
    try:
        response = requests.post(url, headers=headers, files=files)
        if response.ok:
            return response.content
        else:
            st.warning(f"Clipdrop image generation failed for '{title}'. Status: {response.status_code}")
            st.error(f"Error details: {response.text}")
            return None
    except Exception as e:
        st.error(f"Exception during image generation: {e}")
        return None

# ----------------------------------------------------------------------
# 6. MAIN APP LOGIC (GENERATION & DISPLAY)
# ----------------------------------------------------------------------

if generate_btn:
    if not domain.strip():
        st.warning("Please enter a domain/field before generating ideas.")
    else:
        with st.spinner("Forging ideas with OpenAI..."):
            # NEW: Pass difficulty to the generation function
            ideas = generate_ideas(
                domain=domain.strip(), 
                n=num_ideas, 
                model_name=model_choice, 
                temperature=temperature, 
                max_tokens=max_tokens,
                difficulty=difficulty  # Pass the new parameter
            )
            
            if ideas:
                st.session_state.ideas = ideas
                st.success(f"{len(ideas)} ideas forged!")
                st.balloons()
            else:
                st.error("No ideas returned. Try adjusting temperature or model.")

# ---
# DISPLAY LOGIC
# ---
if st.session_state.ideas:
    st.markdown(f"---")
    
    current_domain_display = domain if domain else "Your Ideas"
    st.markdown(f"### Results for **{current_domain_display}**")
    
    cols = st.columns(1 if len(st.session_state.ideas) == 1 else 2)
    
    for idx, idea in enumerate(st.session_state.ideas):
        col_index = idx % (1 if len(st.session_state.ideas) == 1 else 2)
        
        with cols[col_index]:
            # NEW: We use the "st.expander" as the "card" container
            with st.expander(f"**Idea {idx+1}: {idea.get('title','Untitled')}**", expanded=True):
                st.write(f"**Problem:** {idea.get('problem_statement','')}")
                
                tools = idea.get('tools', [])
                if isinstance(tools, list):
                    st.write("**Tools & Tech:** " + ", ".join(tools))
                else:
                    st.write("**Tools & Tech:** " + str(tools))
                
                st.write("**Extension:** " + idea.get('possible_extension',''))
                
                score = idea.get('creativity_score', None)
                if isinstance(score, int):
                    st.write(f"**Creativity Score:** {score}/10")
                    st.progress(min(max(score, 0), 10) * 10)
                
                if include_images:
                    if "image_data" not in idea:
                        if st.button(f"Generate Image", key=f"img_btn_{idx}"):
                            with st.spinner("Generating concept image..."):
                                image_bytes = generate_image_for_idea(idea.get("title",""), idea.get("problem_statement",""))
                                st.session_state.ideas[idx]["image_data"] = image_bytes
                                st.rerun()
                    else:
                        image_data = idea.get("image_data")
                        if image_data:
                            st.image(image_data, caption=f"Concept: {idea.get('title','')}", use_container_width=True)
                        else:
                            st.caption("Image generation failed.")
                
                # NEW: Add a "Copy" block for the raw JSON data
                st.markdown("---")
                st.write("**Copy Idea as JSON:**")
                st.code(json.dumps(idea, indent=2), language="json")
                            
    # ---
    # DOWNLOAD BUTTON
    # ---
    st.markdown("---")
    st.download_button(
        "Download Ideas as JSON",
        data=json.dumps(st.session_state.ideas, indent=2, default=str),
        file_name=f"ideaforge_ideas.json",
        mime="application/json"
    )