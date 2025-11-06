import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Oracle's personality prompt
ORACLE_PERSONALITY = """You are the Oracle of Oddities, a mystical fortune teller with a quirky sense of humor.
You speak in a dramatic, mysterious way but with unexpected comedic twists.
You ask weird, funny questions before revealing fortunes.
Keep responses concise but entertaining (2-3 sentences max for questions, 3-4 for fortunes)."""

def generate_oracle_questions(topic, num_questions=2):
    """Generate funny follow-up questions based on the chosen topic."""
    
    prompt = f"""As the Oracle of Oddities, generate {num_questions} absurd but funny questions 
    related to '{topic}'. Make them personality-based and unexpected.
    
    Format: Return ONLY the questions, numbered 1. and 2., nothing else."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": ORACLE_PERSONALITY},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=200
        )
        
        questions_text = response.choices[0].message.content.strip()
        # Split into list and clean
        questions = [q.strip() for q in questions_text.split('\n') if q.strip() and len(q.strip()) > 3]
        return questions[:num_questions]
        
    except Exception as e:
        return [f"Error: {str(e)}", "Please check your API key and internet connection."]

def generate_fortune(topic, answers):
    """Generate the final fortune based on topic and user answers."""
    
    answers_text = "\n".join([f"Answer {i+1}: {ans}" for i, ans in enumerate(answers)])
    
    prompt = f"""Based on these answers about '{topic}':

{answers_text}

As the Oracle of Oddities, reveal a humorous, creative fortune. 
Make it dramatic yet funny, specific to their answers, and end with a mystical twist.
Keep it to 3-4 sentences maximum."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": ORACLE_PERSONALITY},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=300
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"The spirits are disturbed... Error: {str(e)}"

def get_oracle_greeting():
    """Return the Oracle's greeting message."""
    return """🔮 **Welcome, mortal, to the Oracle of Oddities!** 🔮

I peer beyond the veil of reality... and also enjoy a good meme.

What mysteries shall I unravel for you today?"""
