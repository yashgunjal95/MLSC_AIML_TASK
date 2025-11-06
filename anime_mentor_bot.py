from google import genai

# DIRECT API KEY (local testing only — remove before GitHub)
client = genai.Client(api_key="AIzaSyBszRLtwjYrRAXSlDI14sM1zQGaci0kLec")

def anime_mentor_response(user_input):
    system_prompt = """
You are Anime Mentor Bot, inspired by Kakashi, Gojo, Aizen, and Itachi.
Your tone:
- Calm
- Short sentences
- Mentor-like
- Sharp metaphors
- No cringe
"""

    prompt = system_prompt + "\nUser: " + user_input

    result = client.models.generate_content(
        model="models/gemini-2.5-flash",   # ✅ FREE MODEL
        contents=prompt
    )

    return result.text

def chat_loop():
    print("=== Anime Mentor Bot 🌩️ ===")
    print("Speak your thoughts, young warrior...\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Mentor: Our paths part here. Walk with purpose.")
            break

        reply = anime_mentor_response(user_input)
        print("\nMentor:", reply, "\n")

if __name__ == "__main__":
    chat_loop()
