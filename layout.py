import reflex as rx
from gemini import generate as generate_recipe, extract_steps
from image import generate as generate_image

# Define the app state
class State(rx.State):
    prefs = ""
    steps = []
    current_step = 0
    image_url = ""

    def generate_recipe(self):
        # Use gemini.py to generate the recipe
        recipe_text = generate_recipe(self.prefs)
        self.steps = extract_steps(recipe_text)
        self.current_step = 0
        self.update_image()

    def update_image(self):
        # Use image.py to generate an image for the current step
        step_text = self.steps[self.current_step]
        self.image_url = generate_image(step_text)

    def next_step(self):
        # Move to the next step and update the image
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_image()

# Layout
def layout():
    return rx.box(
        # Title
        rx.heading("Recipe Generator", size="2xl", padding="20px"),

        # Preferences input field
        rx.input(
            placeholder="Enter your recipe preferences...",
            value=State.prefs,  # No need for bind
            on_change=State.set_prefs,
            width="100%",
            padding="10px",
        ),

        # Generate button
        rx.button("Generate", on_click=State.generate_recipe, width="100%", padding="10px", margin_top="10px"),

        # Display the current step
        rx.cond(
            State.steps,
            rx.box(
                rx.heading(f"Step {State.current_step + 1}: {State.steps[State.current_step]}", size="md"),
                rx.image(src=State.image_url, alt="Generated image", width="300px", height="300px"),
                rx.button("Next", on_click=State.next_step, width="100px", padding="10px", margin_top="20px"),
            ),
        ),

        # Center the content
        display="flex",
        flex_direction="column",
        align_items="center",
        justify_content="center",
        padding="50px",
    )

# Reflex App
app = rx.App()
app.add_page(layout)
