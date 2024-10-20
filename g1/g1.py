import groq
import time
import os
import json

client = groq.Groq()


def make_api_call(messages, max_tokens, is_final_answer=False, custom_client=None):
    global client
    if custom_client != None:
        client = custom_client

    for attempt in range(3):
        try:
            if is_final_answer:
                response = client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.2,
                )
                return response.choices[0].message.content
            else:
                response = client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.2,
                    response_format={"type": "json_object"},
                )
                return json.loads(response.choices[0].message.content)
        except Exception as e:
            if attempt == 2:
                if is_final_answer:
                    return {
                        "title": "Error",
                        "content": f"Failed to generate final answer after 3 attempts. Error: {str(e)}",
                    }
                else:
                    return {
                        "title": "Error",
                        "content": f"Failed to generate step after 3 attempts. Error: {str(e)}",
                        "next_action": "final_answer",
                    }
            time.sleep(1)  # Wait for 1 second before retrying


def generate_response(prompt, custom_client=None):
    messages = [
        {
            "role": "system",
            "content": """You are a cooking expert AI assistant named Gordon. You provide assistance for people that are cooking at home. You are going to be given a single step in an already decided recipe. You are going to evaluate the step and give more details about it. FIRST GIVE WHAT THE USER GOING TO BE DOING IN THIS STEP IN YOUR OWN WORDS BRIEFLY. Also give a brief sentence about the reasoning behind going through this step. DO NOT STEP OUTSIDE THE STEP THAT YOU ARE GIVEN. DO NOT SIDETRACK. DO NOT REPEAT YOUR YOURSELF. CHECK IF YOU REPEAT YOURSELF. ACTUALLY CHECK IF EVERY SENTENCE OF YOUR OUTPUTS ADDS A NEW DIMENSION TO YOUR ANSWER. Do not break the chain and jump to next step. You are always going to address the user. Do not use "we" in your answers. Make sure to stay focused on the step that you are going to explain. DO NOT MAKE YOUR ANSWERS TOO LONG. For each step, provide a very brief introduction that describes what you're doing in that step, along with the actual content. For the initial step greet the user and say your name. Decide if you need another step or if you're ready to give the final answer. Respond in JSON format with 'title', 'content', and 'next_action' (either 'continue' or 'final_answer') keys. USE AS MANY REASONING STEPS AS POSSIBLE. MAX 3. BE AWARE OF YOUR LIMITATIONS AS AN LLM AND WHAT YOU CAN AND CANNOT DO. IN YOUR REASONING, INCLUDE EXPLORATION OF ALTERNATIVE ANSWERS. CONSIDER YOU MAY BE WRONG, AND IF YOU ARE WRONG IN YOUR REASONING, WHERE IT WOULD BE. FULLY TEST ALL OTHER POSSIBILITIES. YOU CAN BE WRONG. WHEN YOU SAY YOU ARE RE-EXAMINING, ACTUALLY RE-EXAMINE, AND USE ANOTHER APPROACH TO DO SO. DO NOT JUST SAY YOU ARE RE-EXAMINING. USE AT LEAST 3 METHODS TO DERIVE THE ANSWER. USE BEST PRACTICES. DO NOT REPEAT YOURSELF. DO NOT MAKE YOUR ANSWERS HARD TO READ AND TOO LONG. DO NOT REPEAT YOURSELF! MAKE SURE EVERY ANSWER THAT YOU SPIT OUT LOOKS LIKE EACH OTHER. LIMIT YOUR ANSWER TO MAXIMUM 6 SENTENCES.

Example of a valid JSON response:
```json
{
    "title": "Identifying Key Information",
    "content": "In this step, you're going to fluff the rice with a fork to separate the grains. This is necessary to ensure the rice doesn't clump together and to create a light, fluffy texture. By fluffing the rice, you're also helping to release any excess steam that may have built up during cooking, which can make the rice taste soggy or sticky.",
    "next_action": "continue"
}```
""",
        },
        {"role": "user", "content": prompt},
        {
            "role": "assistant",
            "content": "Thank you! I will now think step by step following my instructions, starting at the beginning after decomposing the problem.",
        },
    ]

    steps = []
    step_count = 1
    total_thinking_time = 0

    while True:
        start_time = time.time()
        step_data = make_api_call(messages, 300, custom_client=custom_client)
        end_time = time.time()
        thinking_time = end_time - start_time
        total_thinking_time += thinking_time

        steps.append(
            (
                f"Step {step_count}: {step_data['title']}",
                step_data["content"],
                thinking_time,
            )
        )

        messages.append({"role": "assistant", "content": json.dumps(step_data)})

        if (
            step_data["next_action"] == "final_answer" or step_count > 25
        ):  # Maximum of 25 steps to prevent infinite thinking time. Can be adjusted.
            break

        step_count += 1

        # Yield after each step for Streamlit to update
        yield steps, None  # We're not yielding the total time until the end

    # Generate final answer
    messages.append(
        {
            "role": "user",
            "content": "Please provide the final answer based solely on your reasoning above. Do not use JSON formatting. Only provide the text response without any titles or preambles. Retain any formatting as instructed by the original prompt, such as exact formatting for free response or multiple choice.",
        }
    )

    start_time = time.time()
    final_data = make_api_call(
        messages, 1200, is_final_answer=True, custom_client=custom_client
    )
    end_time = time.time()
    thinking_time = end_time - start_time
    total_thinking_time += thinking_time

    steps.append(("Final Answer", final_data, thinking_time))

    yield steps, total_thinking_time
