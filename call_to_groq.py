from gemini import extracted
from g1.g1 import generate_response


def groqify(step):
    def main(prompt="give me a pasta recipe"):
        final_message = None

        # Iterate through the generator to get the final message
        for steps, total_thinking_time in generate_response(prompt):
            for title, content, thinking_time in steps:
                if title.startswith("Final Answer"):
                    final_message = content

        # Print the final message
        if final_message:
            return final_message

    return main(step)


def groq_output_whole_thing(prefs="make me a pasta"):
    print("Generating recipe based on preferences...")
    the_recipe = extracted(prefs)
    final_string = ""
    tuple_of_output = (groqify(step) for step in the_recipe)
    for step in tuple_of_output:
        final_string = final_string + step + "\n"
    return final_string


def groq_output_everthing_as_text_file(prefs="make me pasta"):
    with open("groq_output.txt", "w") as file:
        file.write(groq_output_whole_thing(prefs))
        print("the file is created, the function is working fine")
    return "successfully created the file"


"""

!!! IMPORTANT !!!
this is a failed idea that shouldn't be used in the final implementation

"""
