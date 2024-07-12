import google.generativeai as genai
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
t = os.environ['GIMINI_API_KEY']
def generateAI(command:str):
    genai.configure(api_key=t)


    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    response = model.generate_content(command)
    print(response.text)
    return response.text
