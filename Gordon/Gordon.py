import reflex as rx
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini import generate as generate_recipe, extract_steps, extract_ingredients, extract_des, extract_name
from image import generate as generate_image, generate_food

# Define the app state
class State(rx.State):
    prefs = ""
    name = ""
    description=""
    steps = []
    ingredients=[]
    current_step = 0
    generated_steps = 0
    total_steps = 0
    image_url = ""
    images=[]
    food_url=""


    def generate_recipe(self):
        # Use gemini.py to generate the recipe
        recipe_text = generate_recipe(self.prefs)
        self.name = extract_name(recipe_text)
        self.description = extract_des(recipe_text)
        recipe_image = generate_food(self.name, self.description)
        self.food_url = recipe_image
        self.steps = extract_steps(recipe_text)
        self.ingredients = extract_ingredients(recipe_text)
        self.current_step = 0
        self.total_steps = len(self.steps)
        self.update_image()
        print(self.name)
        print(self.description)
        print(self.ingredients)
        print(self.steps)
        return rx.redirect(
            "/recipe"
        )

    def update_image(self):
        # Use image.py to generate an image for the current step
        if self.steps:
            step_text = self.steps[self.current_step]
            self.image_url = generate_image(step_text)
            self.images.append(self.image_url)

    def next_step(self):
        # Move to the next step and update the image
        if self.current_step < len(self.steps) - 1:
            if self.current_step == self.generated_steps:
                self.current_step += 1
                self.generated_steps += 1
                self.update_image()
            else:
                self.current_step += 1
                self.image_url = self.images[self.current_step]

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.image_url = self.images[self.current_step]

def create_input_textarea():
    return rx.box(
        rx.input(
            class_name="border-[#C76A45] focus:ring-[#F56A4B]",
            placeholder="Enter information such as ingredients, dietary restrictions, general preferences, or anything else related to what you would like to cook",
            border_width="1px",
            background_color="#ffffff",
            color="000000",
            _placeholder={
                "color": "#000000",  # Set the placeholder text color to gray
            },
            _focus={
                "outline-style": "none",
                "box-shadow": "var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color)",
            },
            height="8rem",
            padding="0.75rem",
            resize="none",
            border_radius="0.375rem",
            width="100%",
            on_change=State.set_prefs,  # Bind to the State.prefs
        ),
        position="relative",
    )


def create_submit_button():
    return rx.button(
        "Submit",
        class_name="bg-amber-500 hover:bg-amber-600",
        transition_duration="300ms",
        margin_top="1rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_radius="0.375rem",
        color="#ffffff",
        width="100%",
        on_click=State.generate_recipe,  # Trigger recipe generation
    )


def create_form_container():
    return rx.box(
        rx.heading(
            "Gordon",
            class_name="text-amber-500",
            font_weight="700",
            margin_bottom="1.5rem",
            font_size="2.25rem",
            line_height="2.5rem",
            text_align="center",
            as_="h1",
        ),
        rx.text(
            "Enter your preferences here",
            class_name="text-[#8B4513]",
            margin_bottom="1rem",
            text_align="center",
            font_size="1.125rem",
            line_height="1.75rem",
        ),
        create_input_textarea(),
        create_submit_button(),
        background_color="#ffffff",
        max_width="28rem",
        padding="2rem",
        border_radius="0.5rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        width="100%",
    )


def render_main_page():
    """Renders the main page of the Gordon application, including styles, layout, and content."""
    return rx.fragment(
        rx.script(src="https://cdn.tailwindcss.com"),
        rx.el.style(
            """
        @font-face {
            font-family: 'LucideIcons';
            src: url(https://unpkg.com/lucide-static@latest/font/Lucide.ttf) format('truetype');
        }
    """
        ),
        rx.box(
            create_form_container(),
            class_name="bg-[#F5F2EF]",
            display="flex",
            align_items="center",
            justify_content="center",
            min_height="100vh",
        ),
    )

def create_icon(icon_height, icon_tag, icon_width):
    """Create an icon with specified height, tag, and width."""
    return rx.icon(
        tag=icon_tag,
        height=icon_height,
        margin_right="0.5rem",
        width=icon_width,
    )


def create_button_link(link_url, icon_tag, button_text):
    """Create a button-style link with an icon and text."""
    return rx.el.a(
        create_icon(
            icon_height="1rem",
            icon_tag=icon_tag,
            icon_width="1rem",
        ),
        button_text,
        href=link_url,
        class_name="bg-amber-500 hover:bg-amber-600",
        font_weight="700",
        display="inline-flex",
        align_items="center",
        padding_left="1rem",
        padding_right="1rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_radius="0.25rem",
        color="#ffffff",
    )


def create_heading_with_icon(icon_tag, heading_text):
    """Create a heading with an icon and specified text."""
    return rx.heading(
        create_icon(
            icon_height="1.5rem",
            icon_tag=icon_tag,
            icon_width="1.5rem",
        ),
        heading_text,
        class_name="text-amber-700",
        display="flex",
        font_weight="600",
        align_items="center",
        margin_bottom="1.5rem",
        font_size="1.5rem",
        line_height="2rem",
        as_="h2",
    )


def create_list_item(item_text):
    """Create a list item with the given text."""
    return rx.el.li(item_text)


def create_ingredients_list():
    """Create a list of ingredients for spaghetti carbonara."""
    return rx.list(
        rx.foreach(State.ingredients, lambda ingredient: create_list_item(item_text=ingredient)),
        class_name="text-amber-900",
        display="flex",
        flex_direction="column",
        list_style_type="disc",
        list_style_position="inside",
        gap="0.5rem",
    )


def create_ingredients_section():
    """Create the ingredients section with image and list."""
    return rx.box(
        rx.image(
            alt="A plate of creamy spaghetti carbonara with crispy bacon bits and a sprinkle of fresh parsley",
            src=State.food_url,
            margin_bottom="2rem",
            border_radius="0.5rem",
            box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
            width="100%",
        ),
        rx.box(
            create_heading_with_icon(
                icon_tag="utensils",
                heading_text=" Ingredients ",
            ),
            create_ingredients_list(),
            background_color="#ffffff",
            padding="2rem",
            border_radius="0.5rem",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        ),
        grid_column=rx.breakpoints(
            {"1024px": "span 1 / span 1"}
        ),
    )


def create_instructions_list():
    """Create an ordered list of cooking instructions for spaghetti carbonara."""
    return rx.list.ordered(
        rx.foreach(State.steps, lambda step: create_list_item(item_text=step)),
        class_name="text-amber-900",
        display="flex",
        flex_direction="column",
        list_style_type="decimal",
        list_style_position="inside",
        gap="1rem",
    )


def create_instructions_section():
    """Create the instructions section with steps and exit button."""
    return rx.box(
        rx.box(
            create_heading_with_icon(
                icon_tag="info",
                heading_text=" Description ",
            ),
            rx.text(
                State.description,
                class_name="text-amber-900",
            ),
            background_color="#ffffff",
            margin_bottom="2rem",
            padding="2rem",
            border_radius="0.5rem",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        ),
        rx.box(
            create_heading_with_icon(
                icon_tag="book-open",
                heading_text=" Instructions ",
            ),
            create_instructions_list(),
            rx.box(
                create_button_link(
                    link_url="/",
                    icon_tag="x",
                    button_text=" Exit ",
                ),
                margin_top="2rem",
                text_align="center",
            ),
            id="instructions",
            background_color="#ffffff",
            padding="2rem",
            border_radius="0.5rem",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        ),
    )


def create_recipe_page_main():
    """Create the main recipe page layout with all sections."""
    return rx.box(
        rx.heading(
            State.name,
            class_name="text-amber-800",
            font_weight="700",
            margin_bottom="2rem",
            font_size="3rem",
            line_height="1",
            text_align="center",
            as_="h1",
        ),
        rx.box(
            create_button_link(
                link_url="/recipe_steps",
                icon_tag="play",
                button_text=" Start Cooking ",
            ),
            margin_bottom="2rem",
            text_align="center",
        ),
        rx.box(
            create_ingredients_section(),
            rx.box(
                create_instructions_section(),
                grid_column=rx.breakpoints(
                    {"1024px": "span 1 / span 1"}
                ),
            ),
            gap="3rem",
            display="grid",
            grid_template_columns=rx.breakpoints(
                {"1024px": "repeat(2, minmax(0, 1fr))"}
            ),
        ),
        rx.box(
            rx.text(
                f"Enjoy your homemade {State.name}!",
                class_name="text-amber-700",
                font_style="italic",
                font_size="1.125rem",
                line_height="1.75rem",
            ),
            margin_top="3rem",
            text_align="center",
        ),
        width="100%",
        style=rx.breakpoints(
            {
                "640px": {"max-width": "640px"},
                "768px": {"max-width": "768px"},
                "1024px": {"max-width": "1024px"},
                "1280px": {"max-width": "1280px"},
                "1536px": {"max-width": "1536px"},
            }
        ),
        margin_left="auto",
        margin_right="auto",
        padding_left="1rem",
        padding_right="1rem",
        padding_top="3rem",
        padding_bottom="3rem",
        background_color="#ffffff",
    )


def create_app_layout():
    """Create the overall app layout with styling and content."""
    return rx.fragment(
        rx.el.link(
            href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
            rel="stylesheet",
        ),
        rx.el.style(
            """
        @font-face {
            font-family: 'LucideIcons';
            src: url(https://unpkg.com/lucide-static@latest/font/Lucide.ttf) format('truetype');
        }
    """
        ),
        rx.box(
            create_recipe_page(),
            background_color="#FFFBEB",
            font_family='system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
        ),
    )

def create_icon_step(icon_name):
    """Create an icon with specified dimensions and margin."""
    return rx.icon(
        tag=icon_name,
        height="1.5rem",
        margin_right="0.5rem",
        width="1.5rem",
    )


def create_previous_step_button():
    """Create a styled 'Previous Step' button with a chevron-left icon."""
    return rx.el.button(
        create_icon_step(icon_name="chevron-left"),
        " Previous Step ",
        class_name="bg-amber-600 hover:bg-amber-700",
        transition_duration="300ms",
        display="flex",
        font_weight="700",
        align_items="center",
        padding_left="1.5rem",
        padding_right="1.5rem",
        padding_top="0.75rem",
        padding_bottom="0.75rem",
        border_radius="0.5rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        color="#ffffff",
        transition_property="background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
        transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
    )


def create_exit_recipe_button():
    """Create a styled 'Exit Recipe' button with an X icon."""
    return rx.el.button(
        create_icon_step(icon_name="x"),
        " Exit Recipe ",
        background_color="#DC2626",
        transition_duration="300ms",
        display="flex",
        font_weight="700",
        _hover={"background-color": "#B91C1C"},
        align_items="center",
        padding_left="1.5rem",
        padding_right="1.5rem",
        padding_top="0.75rem",
        padding_bottom="0.75rem",
        border_radius="0.5rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        color="#ffffff",
        transition_property="background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
        transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
        on_click=rx.redirect("/")
    )


def create_next_step_button():
    """Create a styled 'Next Step' button with a chevron-right icon."""
    return rx.el.button(
        " Next Step ",
        rx.icon(
            tag="chevron-right",
            height="1.5rem",
            margin_left="0.5rem",
            width="1.5rem",
        ),
        background_color="#059669",
        transition_duration="300ms",
        display="flex",
        font_weight="700",
        _hover={"background-color": "#047857"},
        align_items="center",
        padding_left="1.5rem",
        padding_right="1.5rem",
        padding_top="0.75rem",
        padding_bottom="0.75rem",
        border_radius="0.5rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        color="#ffffff",
        transition_property="background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
        transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
    )


def create_recipe_step():
    """Create a dynamic recipe step component with heading, instructions, image, and navigation buttons."""
    return rx.box(
        # Heading for the current step number
        rx.heading(
            f"Step {State.current_step + 1}/{State.total_steps}: {State.steps[State.current_step]}",  # Dynamic step title
            class_name="text-amber-700",
            font_weight="600",
            margin_bottom="1rem",
            font_size="1.875rem",
            line_height="2.25rem",
            text_align="center",
            as_="h2",
        ),
        
        # Image for the current step
        rx.image(
            alt=f"Image for Step {State.current_step + 1}",
            src=State.image_url,  # Dynamic image URL
            margin_bottom="2rem",
            border_radius="0.5rem",
            box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
            width="100%",
        ),
        
        # Flexbox for Previous, Exit, and Next buttons
        rx.flex(
            # Previous Step button (disabled on the first step)
            rx.cond(State.current_step > 0,  # Only show if not on the first step
                rx.button(
                    create_icon_step(icon_name="chevron-left"),
                    " Previous Step ",
                    class_name="bg-amber-600 hover:bg-amber-700",
                    transition_duration="300ms",
                    display="flex",
                    font_weight="700",
                    align_items="center",
                    padding_left="1.5rem",
                    padding_right="1.5rem",
                    padding_top="0.75rem",
                    padding_bottom="0.75rem",
                    border_radius="0.5rem",
                    box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                    color="#ffffff",
                    on_click=State.previous_step  # Previous step logic
                ),
            ),
            
            # Exit Recipe button (always shown)
            create_exit_recipe_button(),
            
            # Next Step button (disabled on the last step)
            rx.cond(State.steps,  # Only show if not on the last step
                rx.button(
                    " Next Step ",
                    create_icon_step(icon_name="chevron-right"),
                    class_name="bg-green-600 hover:bg-green-700",
                    transition_duration="300ms",
                    display="flex",
                    font_weight="700",
                    align_items="center",
                    padding_left="1.5rem",
                    padding_right="1.5rem",
                    padding_top="0.75rem",
                    padding_bottom="0.75rem",
                    border_radius="0.5rem",
                    box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                    color="#ffffff",
                    on_click=State.next_step  # Next step logic
                ),
            ),
            display="flex",
            justify_content="space-between",
            margin_top="2rem",
        ),
        
        background_color="#ffffff",
        padding="2rem",
        border_radius="0.5rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    )


def create_recipe_page():
    """Create the main recipe page with a title and dynamic recipe steps."""
    return rx.box(
        rx.heading(
            State.name,  # Dynamic recipe name from State
            class_name="text-amber-800",
            font_weight="700",
            margin_bottom="2rem",
            font_size="3rem",
            line_height="1",
            text_align="center",
            as_="h1",
        ),
        create_recipe_step(),  # Display the current recipe step
        width="100%",
        style=rx.breakpoints(
            {
                "640px": {"max-width": "640px"},
                "768px": {"max-width": "768px"},
                "1024px": {"max-width": "1024px"},
                "1280px": {"max-width": "1280px"},
                "1536px": {"max-width": "1536px"},
            }
        ),
        margin_left="auto",
        margin_right="auto",
        padding_left="1rem",
        padding_right="1rem",
        padding_top="3rem",
        padding_bottom="3rem",
    )

def create_steps_page():
    """Create the overall app layout with styling and recipe page content."""
    return rx.fragment(
        rx.el.link(
            href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
            rel="stylesheet",
        ),
        rx.el.style(
            """
        @font-face {
            font-family: 'LucideIcons';
            src: url(https://unpkg.com/lucide-static@latest/font/Lucide.ttf) format('truetype');
        }
    """
        ),
        rx.box(
            create_recipe_page(),
            background_color="#FFFBEB",
            font_family='system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
        ),
    )

# Reflex App
app = rx.App()

# Add pages to the app
app.add_page(render_main_page, route="/")
app.add_page(create_steps_page, route="/recipe_steps")
app.add_page(create_recipe_page_main, route="/recipe")