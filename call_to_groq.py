#from gemini import extracted
from g1.g1 import generate_response

# this function takes a single element of an array and groqfy's it
def groqify(step='this is the initial step of the cooking process. try to relax before doing anything'):
    #this function calls the groq api and gets the final answer
    print("GROQIFYING")
    def main(prompt):
        final_message = None

        # Iterate through the generator to get the final message
        for steps, total_thinking_time in generate_response(prompt):
            for title, content, thinking_time in steps:
                if title.startswith("Final Answer"):
                    final_message = content
        # Print the final message
        if final_message:
            print(final_message)
            return final_message
            
    return main(step)

