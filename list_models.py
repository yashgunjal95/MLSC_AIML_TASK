from google import genai
client = genai.Client(api_key="AIzaSyBszRLtwjYrRAXSlDI14sM1zQGaci0kLec")

models = client.models.list()

for m in models:
    print(m.name)
