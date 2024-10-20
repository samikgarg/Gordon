import google.generativeai as genai
import os
import re

def generate(prefs):
    genai.configure(api_key=os.environ["API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Hi, I have a certain list of preferences, based on which I want to cook a dish. Here are my preferences: {prefs}. Do not give me an ingredients list. Please come up with a dish and describe that dish in detail based on these preferences. Then, please generate a detailed step by step recipe that can be followed to cook that dish exactly. Make sure it is very detailed and specific. The recipe must be separated into clear steps. Please start each step with <step> and end each step with </step>. One step has to be a continuous sentence or paragraph, it must not have listing in it.")
    return response.text

def extract_steps(text):
    steps = re.findall(r'<step>(.*?)</step>', text)
    return [f"Step {i+1}/{len(steps)}: {step}" for i, step in enumerate(steps)]
    
#print(generate('i want to make a pasta with tomato sauce and onions. I want the pasta to be spicy and please make sure that it is not salty.'))
#steps = generate("I am kinda feeling a spicy dish. I have a couple tomatoes and some rice in the fridge and I want to use it. I am alergic to nuts. I want to eat something tasty that I can make with low effort.")
#steps_arr = extract_steps(steps)
#for i, step in enumerate(steps_arr):
    #print(f"Step {i+1}/{len(steps_arr)}: {step}")
    #input()

    