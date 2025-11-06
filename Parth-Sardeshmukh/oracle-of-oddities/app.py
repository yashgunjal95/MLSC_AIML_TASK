import streamlit as st
from oracle_logic import generate_oracle_questions, generate_fortune, get_oracle_greeting

# Page config
st.set_page_config(
    page_title="Oracle of Oddities",
    page_icon="🔮",
    layout="centered"
)

# Custom CSS for mystical vibes
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e0033 0%, #0a0015 100%);
    }
    .stButton>button {
        background-color: #6b46c1;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-size: 16px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #553c9a;
    }
    .fortune-box {
        background-color: rgba(107, 70, 193, 0.2);
        border: 2px solid #8b5cf6;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'stage' not in st.session_state:
    st.session_state.stage = 'welcome'
    st.session_state.topic = None
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.current_question = 0
    st.session_state.fortune = None

# Title
st.title("🔮 The Oracle of Oddities")
st.markdown("*A mystical fortune teller with questionable credentials*")
st.markdown("---")

# STAGE 1: Welcome & Topic Selection
if st.session_state.stage == 'welcome':
    st.markdown(get_oracle_greeting())
    st.markdown("### Choose your destiny's domain:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📚 GPA This Semester"):
            st.session_state.topic = "GPA this semester"
            st.session_state.stage = 'loading'
            st.rerun()
        
        if st.button("💼 Future Career"):
            st.session_state.topic = "Future career"
            st.session_state.stage = 'loading'
            st.rerun()
        
        if st.button("😴 Sleep Schedule"):
            st.session_state.topic = "Sleep schedule"
            st.session_state.stage = 'loading'
            st.rerun()
    
    with col2:
        if st.button("❤️ Love Life"):
            st.session_state.topic = "Love life"
            st.session_state.stage = 'loading'
            st.rerun()
        
        if st.button("🫶 Social Life"):
            st.session_state.topic = "Social life"
            st.session_state.stage = 'loading'
            st.rerun()
    
    st.markdown("### Or enter your own mystical query:")
    custom_topic = st.text_input("What do you seek to know?", placeholder="e.g., My exam results, Weekend plans...")
    
    if st.button("🌟 Consult the Oracle"):
        if custom_topic:
            st.session_state.topic = custom_topic
            st.session_state.stage = 'loading'
            st.rerun()
        else:
            st.warning("Please enter a topic or choose from above!")

# STAGE 2: Loading Questions
elif st.session_state.stage == 'loading':
    with st.spinner("✨ The Oracle consults the cosmic energies..."):
        st.session_state.questions = generate_oracle_questions(st.session_state.topic)
        st.session_state.stage = 'questions'
        st.session_state.current_question = 0
        st.session_state.answers = []
    st.rerun()

# STAGE 3: Ask Questions
elif st.session_state.stage == 'questions':
    st.markdown(f"### 🔮 Reading: *{st.session_state.topic}*")
    st.markdown("---")
    
    # Show current question
    q_num = st.session_state.current_question
    if q_num < len(st.session_state.questions):
        st.markdown(f"### Question {q_num + 1} of {len(st.session_state.questions)}")
        st.markdown(f"#### {st.session_state.questions[q_num]}")
        
        answer = st.text_area(
            "Your answer:",
            key=f"answer_{q_num}",
            placeholder="The spirits await your response...",
            height=100
        )
        
        if st.button("Submit Answer 🌙"):
            if answer.strip():
                st.session_state.answers.append(answer)
                st.session_state.current_question += 1
                
                # Check if done with questions
                if st.session_state.current_question >= len(st.session_state.questions):
                    st.session_state.stage = 'generating_fortune'
                
                st.rerun()
            else:
                st.warning("The Oracle requires an answer to proceed!")
        
        # Show progress
        st.progress(q_num / len(st.session_state.questions))

# STAGE 4: Generate Fortune
elif st.session_state.stage == 'generating_fortune':
    with st.spinner("🌟 The Oracle peers into the fabric of reality..."):
        st.session_state.fortune = generate_fortune(
            st.session_state.topic,
            st.session_state.answers
        )
        st.session_state.stage = 'reveal'
    st.rerun()

# STAGE 5: Reveal Fortune
elif st.session_state.stage == 'reveal':
    st.markdown(f"### 🔮 Your Fortune Regarding: *{st.session_state.topic}*")
    st.markdown("---")
    
    st.markdown(f"""
    <div class="fortune-box">
        <h3 style="text-align: center; color: #d8b4fe;">✨ The Oracle Speaks ✨</h3>
        <p style="font-size: 18px; line-height: 1.8; color: #e9d5ff; text-align: center;">{st.session_state.fortune}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Ask Another Question"):
            # Reset everything
            st.session_state.stage = 'welcome'
            st.session_state.topic = None
            st.session_state.questions = []
            st.session_state.answers = []
            st.session_state.current_question = 0
            st.session_state.fortune = None
            st.rerun()
    
    with col2:
        # Create downloadable fortune
        fortune_text = f"""
🔮 THE ORACLE OF ODDITIES 🔮
━━━━━━━━━━━━━━━━━━━━━━━━━

Topic: {st.session_state.topic}

Your Fortune:
{st.session_state.fortune}

━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by The Oracle of Oddities
        """
        
        st.download_button(
            label="💾 Save Fortune",
            data=fortune_text,
            file_name="my_fortune.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #9ca3af;'><em>The Oracle of Oddities takes no responsibility for the accuracy of these predictions... or anything, really.</em></p>", unsafe_allow_html=True)
