#AIzaSyDa-Kku4QD4buM0gJyynhWW0SsfD1DncJ8

import google.generativeai as genai
import os
import re

def generate(prefs):
    genai.configure(api_key=os.environ["API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Hi, I have a certain list of preferences, based on which I want to cook a dish. Here are my preferences: {prefs}. Please come up with a dish and describe that dish in detail based on these preferences. Then, please generate a comprehensive ingredients list for that recipe. Then, please generate a detailed step by step recipe that can be followed to cook that dish exactly. Make sure it is very detailed and specific. The recipe must be separated into clear steps. Please put <name> before the name of the dish and </name> at the end of the dish name. Please start the description with <des>. Please end the description with </des>. Please start the ingredients list with <ingredients> and end the ingredients list with </ingredients>. Please put <in> before each ingredient and </in> after each ingredient. Please start the steps list with <steps> and end it with </steps>. Please start each step with <step> and end each step with </step>. One step has to be a continuous sentence or paragraph, it must not have listing in it.")
    print(response.text)
    return response.text

#print(generate('I feel like I want to eat past carbonar and I want it to be spicy.'))

def extract_name(text):
    match = re.search(r'<name>(.*?)</name>', text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return "" 

def extract_des(text):
    match = re.search(r'<des>(.*?)</des>', text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return "" 

def extract_ingredients(text):
    ins = re.findall(r'<in>(.*?)</in>', text)
    return [f"{ing}" for ing in ins]

def extract_steps(text):
    steps = re.findall(r'<step>(.*?)</step>', text)
    return [f"{step}" for step in steps]
    

#steps = generate("I am kinda feeling a spicy dish. I have a couple tomatoes and some rice in the fridge and I want to use it. I am alergic to nuts. I want to eat something tasty that I can make with low effort.")
#steps_arr = extract_steps(steps)
#for i, step in enumerate(steps_arr):
    #print(f"Step {i+1}/{len(steps_arr)}: {step}")
    #input()