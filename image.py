from openai import OpenAI

def generate(step):
    client = OpenAI()

    response = client.images.generate(
    model="dall-e-3",
    prompt=f"Here is a step for a recipe: {step} Generate a cartoonish version of Gordon Ramsay. He must be performing these steps in an instructive manner. Ensure that the image clearly shows how this step is done in a comprehensive manner. I want a cartoon image.",
    size="1024x1024",
    quality="standard",
    n=1,
    )
    print(response.data[0].url)
    return response.data[0].url

def generate_food(name, description):
    client = OpenAI()
    response = client.images.generate(
    model="dall-e-3",
    prompt=f"Here is a dish with name: {name} and description: {description}. Please generate a realistic image of this dish",
    size="1024x1024",
    quality="standard",
    n=1,
    )
    print(response.data[0].url)
    return response.data[0].url
#step = input()
#image_url = generate(step)
#print(image_url)
