import streamlit as st
import json
import google.generativeai as genai

# -------------- SETUP --------------
st.set_page_config(page_title="ChatMimic 🤖", page_icon="🎭", layout="centered")

# Load personalities
with open("personalities.json", "r") as f:
    personalities = json.load(f)

# Sidebar setup
st.sidebar.title("🎭 Choose Personality")
selected_persona = st.sidebar.selectbox("Select a character:", list(personalities.keys()))

# API key input (for local testing — uses your free Gemini key)
api_key = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")



    st.title("🤖 ChatMimic: The Multi-Personality Chatbot")
    st.write(f"Now chatting as **{selected_persona}** 🗣️")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("💬 You:", placeholder="Type your message here...")

    if st.button("Send") and user_input:
        persona_prompt = personalities[selected_persona]
        prompt = f"{persona_prompt}\nUser: {user_input}\n{selected_persona}:"

        response = model.generate_content(prompt)
        reply = response.text

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append((selected_persona, reply))

    # Display chat
    for speaker, message in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"**🧑‍💻 You:** {message}")
        else:
            st.markdown(f"**🎭 {speaker}:** {message}")
else:
    st.warning("Please enter your Gemini API key in the sidebar to start chatting.")
