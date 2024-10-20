#5ff06bfd-f4ab-4672-9ccc-3433ff69d488

import reflex as rx
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini import generate as generate_recipe, extract_steps, extract_ingredients, extract_des, extract_name
from image import generate as generate_image, generate_food
from call_to_groq import groqify
from text_to_speech import speak_transcript
import concurrent.futures
import threading

# Define the app state
class State(rx.State):
    prefs = ""
    name = ""
    description=""
    steps = []
    groqified_steps=[]
    ingredients=[]
    current_step = -1
    generated_steps = -1
    total_steps = 0
    image_url = ""
    current_groq_step = ""
    images=[]
    food_url=""
    started = True


    def generate_recipe(self):
        # Use gemini.py to generate the recipe
        #speak_transcript("test")
        def init_steps():
            recipe_text = generate_recipe(self.prefs)
            self.name = extract_name(recipe_text)
            self.description = extract_des(recipe_text)
            self.steps = extract_steps(recipe_text)
            self.ingredients = extract_ingredients(recipe_text)
        
        def init_img():
            recipe_image = generate_food(self.name, self.description)
            self.food_url = recipe_image

        init_steps()
        init_img()

        self.current_step = -1
        self.generated_steps = -1
        self.total_steps = len(self.steps)
        self.images = []
        self.groqified_steps = []
        self.started = True
        print(self.name)
        print(self.description)
        print(self.ingredients)
        print(self.steps)
        return rx.redirect(
            "/recipe"
        )
    
    def say_step(self):
        speak_transcript(self.groqified_steps[self.current_step])

    def update_image(self):
        # Use image.py to generate an image for the current step
        if self.steps:
            step_text = self.steps[self.current_step]
            self.image_url = generate_image(step_text)
            self.images.append(self.image_url)
    
    def update_groqified_steps(self):
        if self.steps:
            step_text = f"Step {self.current_step+1}: {self.steps[self.current_step]}"
            self.current_groq_step = groqify(step_text)
            self.groqified_steps.append(self.current_groq_step)

    def exit_recipe(self):
        self.current_step = -1
        return rx.redirect(
            "/recipe"
        )

    def next_step(self):
        # Move to the next step and update the image
        if self.current_step < len(self.steps) - 1:
            if self.current_step == self.generated_steps:
                if (self.started):
                    self.started = False
                self.current_step += 1
                self.generated_steps += 1
                self.update_image()
                self.update_groqified_steps()
                thread = threading.Thread(target=self.say_step)
                thread.start()
            else:
                self.current_step += 1
                self.image_url = self.images[self.current_step]
                self.current_groq_step = self.groqified_steps[self.current_step]

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.image_url = self.images[self.current_step]
            self.current_groq_step = self.groqified_steps[self.current_step]

    def search_on_key_down(self, event):
        # Check if event has a 'key' attribute and if 'Enter' is pressed
        if event == "Enter":
            print("HERERERE")
            return self.generate_recipe()

def create_stylesheet_link(stylesheet_url):
   """Create a link element for a stylesheet."""
   return rx.el.link(href=stylesheet_url, rel="stylesheet")

def create_heading(heading_text):
   """Create an amber-colored heading with specific styling."""
   return rx.heading(
       heading_text,
       class_name="text-amber-700",
       font_weight="700",
       margin_bottom="0.5rem",
       font_size="1.25rem",
       line_height="1.75rem",
       as_="h3",
   )

def create_icon_home(
   alt_text, icon_height, icon_tag, icon_width
):
   """Create an icon element with specified attributes."""
   return rx.icon(
       alt=alt_text,
       tag=icon_tag,
       height=icon_height,
       width=icon_width,
   )

def create_image(alt_text, image_src):
   """Create an image element with specific dimensions and styling."""
   return rx.image(
       alt=alt_text,
       src=image_src,
       height="12rem",
       object_fit="cover",
       width="100%",
   )

def create_styled_text(css_class, text_content):
   """Create a text element with a specified CSS class."""
   return rx.text(text_content, class_name=css_class)

def create_content_box(heading_text, description_text):
   """Create a box containing a heading and description text."""
   return rx.box(
       create_heading(heading_text=heading_text),
       create_styled_text(
           css_class="text-amber-600",
           text_content=description_text,
       ),
       padding="1.5rem",
   )

def create_feature_card(
   image_alt, image_src, card_title, card_description
):
   """Create a feature card with an image, title, and description."""
   return rx.box(
       create_image(
           alt_text=image_alt, image_src=image_src
       ),
       create_content_box(
           heading_text=card_title,
           description_text=card_description,
       ),
       background_color="#ffffff",
       overflow="hidden",
       border_radius="0.75rem",
       box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
   )

def create_social_link(platform_name, icon_tag):
   """Create a social media link with an icon."""
   return rx.el.a(
       create_icon_home(
           alt_text=platform_name,
           icon_height="2rem",
           icon_tag=icon_tag,
           icon_width="2rem",
       ),
       class_name="hover:text-amber-300",
       href="#",
       transition_duration="300ms",
       transition_property="background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
       transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
   )

def create_hero_section():
   """Create the hero section with title and description."""
   return rx.box(
       rx.heading(
           "Gordon",
           class_name="text-amber-700",
           font_weight="700",
           margin_bottom="1rem",
           font_size=rx.breakpoints(
               {"0px": "3rem", "768px": "3.75rem"}
           ),
           line_height=rx.breakpoints(
               {"0px": "1", "768px": "1"}
           ),
           as_="h1",
       ),
       rx.text(
           "Your intelligent culinary companion for recipes, tips, and gastronomic adventures.",
           class_name="text-amber-600",
           max_width="42rem",
           margin_bottom="1.5rem",
           margin_left="auto",
           margin_right="auto",
           font_size="1.25rem",
           line_height="1.75rem",
       ),
       margin_bottom="2rem",
       text_align="center",
   )

def create_search_input():
   """Create a styled search input field."""
   return rx.el.input(
       class_name="focus:ring-amber-500 placeholder-amber-400 text-amber-700",
       placeholder="What would you like to cook today?",
       type="text",
       background_color="#ffffff",
       _focus={
           "outline-style": "none",
           "box-shadow": "var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color)",
       },
       padding_left="2rem",
       padding_right="2rem",
       padding_top="1.25rem",
       padding_bottom="1.25rem",
       border_radius="9999px",
       box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
       font_size="1.25rem",
       line_height="1.75rem",
       width="100%",
       on_change=State.set_prefs,
       on_key_down = State.search_on_key_down,
   )

def create_main_content():
   """Create the main content section including hero, search, and feature cards."""
   return rx.flex(
       create_hero_section(),
       rx.box(
           create_search_input(),
           max_width="48rem",
           margin_bottom="4rem",
           position="relative",
           width="100%",
       ),
       rx.box(
           create_feature_card(
               image_alt="A diverse array of colorful dishes from various cuisines",
               image_src="https://reflex-hosting-dev-flexgen.s3.us-west-2.amazonaws.com/replicate/YeXIIvPqRXye2EWTCtyNCFifYhPPidoZhljHVjlGNpbIpKRnA/out-0.webp",
               card_title="Unlimited Food Options",
               card_description="Explore a vast array of cuisines and dishes from around the world, all at your fingertips.",
           ),
           create_feature_card(
               image_alt="A chef customizing a recipe on a digital tablet",
               image_src="https://reflex-hosting-dev-flexgen.s3.us-west-2.amazonaws.com/replicate/sMS5Vvi2LorTORAJlr5hJFcUpkbbK4xtDHSMUvFlyxBJVJ6E/out-0.webp",
               card_title="Customized Recipes",
               card_description="Get personalized recipes tailored to your dietary preferences, restrictions, and available ingredients.",
           ),
           create_feature_card(
               image_alt="An AI assistant guiding a person through a cooking process",
               image_src="https://reflex-hosting-dev-flexgen.s3.us-west-2.amazonaws.com/replicate/jokcVKjRB1ICDVP3oNBwnRuIz1yg7140B20Gs0m8JnDJVJ6E/out-0.webp",
               card_title="Intelligent AI Guide",
               card_description="Receive step-by-step guidance, cooking tips, and real-time assistance from our advanced AI chef.",
           ),
           gap="2rem",
           display="grid",
           grid_template_columns=rx.breakpoints(
               {
                   "0px": "repeat(1, minmax(0, 1fr))",
                   "768px": "repeat(3, minmax(0, 1fr))",
               }
           ),
           max_width="72rem",
           width="100%",
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
       display="flex",
       flex_direction="column",
       flex_grow="1",
       align_items="center",
       justify_content="center",
       margin_left="auto",
       margin_right="auto",
       padding_left="1.5rem",
       padding_right="1.5rem",
       padding_top="3rem",
       padding_bottom="3rem",
   )

def create_footer_content():
   """Create the footer content with title and description."""
   return rx.box(
       rx.heading(
           "Gordon",
           class_name="text-amber-300",
           font_weight="600",
           margin_bottom="0.5rem",
           font_size="1.5rem",
           line_height="2rem",
           as_="h3",
       ),
       create_styled_text(
           css_class="text-amber-200",
           text_content="Empowering your culinary journey with artificial intelligence",
       ),
       margin_bottom=rx.breakpoints(
           {"0px": "1.5rem", "768px": "0"}
       ),
       width=rx.breakpoints(
           {"0px": "100%", "768px": "50%"}
       ),
   )

def create_footer():
   """Create the footer section with content and social links."""
   return rx.flex(
       create_footer_content(),
       rx.flex(
           rx.flex(
               create_social_link(
                   platform_name="Facebook",
                   icon_tag="facebook",
               ),
               create_social_link(
                   platform_name="Twitter",
                   icon_tag="twitter",
               ),
               create_social_link(
                   platform_name="Instagram",
                   icon_tag="instagram",
               ),
               display="flex",
               column_gap="1.5rem",
           ),
           display="flex",
           justify_content="flex-end",
           width=rx.breakpoints(
               {"0px": "100%", "768px": "50%"}
           ),
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
       display="flex",
       flex_wrap="wrap",
       align_items="center",
       justify_content="space-between",
       margin_left="auto",
       margin_right="auto",
       padding_left="1.5rem",
       padding_right="1.5rem",
   )

def create_page_layout():
   """Create the overall page layout including main content and footer."""
   return rx.box(
       create_main_content(),
       rx.box(
           create_footer(),
           class_name="bg-gradient-to-r from-amber-900 to-amber-950",
           margin_top="4rem",
           padding_top="2.5rem",
           padding_bottom="2.5rem",
           color="#ffffff",
       ),
       class_name="bg-gradient-to-br font-['Inter'] from-amber-100 to-amber-200",
       display="flex",
       flex_direction="column",
       min_height="100vh",
   )

def render_main_page():
   """Create the complete application with styles and layout."""
   return rx.fragment(
       create_stylesheet_link(
           stylesheet_url="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"
       ),
       create_stylesheet_link(
           stylesheet_url="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap"
       ),
       rx.el.style(
           """
       @font-face {
           font-family: 'LucideIcons';
           src: url(https://unpkg.com/lucide-static@latest/font/Lucide.ttf) format('truetype');
       }
   """
       ),
       create_page_layout(),
   )

def create_icon(icon_height, icon_tag, icon_width):
    """Create an icon with specified height, tag, and width."""
    return rx.icon(
        tag=icon_tag,
        height=icon_height,
        margin_right="0.5rem",
        width=icon_width,
    )


def create_button_link(link_url, icon_tag, button_text, onClick=None):
    """Create a button-style link with an icon and text. If onClick is provided, it will override the href behavior."""
    # Set up the common attributes for the button
    button_attributes = {
        "class_name": "bg-amber-500 hover:bg-amber-600",
        "font_weight": "700",
        "display": "inline-flex",
        "align_items": "center",
        "padding_left": "1rem",
        "padding_right": "1rem",
        "padding_top": "0.5rem",
        "padding_bottom": "0.5rem",
        "border_radius": "0.25rem",
        "color": "#ffffff",
    }

    # If onClick is provided, attach it as an event handler, otherwise use the href
    if onClick:
        button_attributes["on_click"] = onClick

    button_attributes["href"] = link_url

    return rx.el.a(
        create_icon(
            icon_height="1rem",
            icon_tag=icon_tag,
            icon_width="1rem",
        ),
        button_text,
        **button_attributes  # Pass the attributes dynamically
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
                onClick = State.next_step
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
        height="3rem",
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
        on_click=State.exit_recipe
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
        height="10rem",
    )


def create_recipe_step():
    """Create a dynamic recipe step component with heading, instructions, image, and navigation buttons."""
    return rx.box(
        # Heading for the current step number
        rx.heading(
            f"Step {State.current_step + 1}/{State.total_steps}",  # Dynamic step title
            class_name="text-amber-700",
            font_weight="600",
            margin_bottom="1rem",
            font_size="1.875rem",
            line_height="2.25rem",
            text_align="center",
            as_="h2",
        ),

        rx.heading(
            f"{State.groqified_steps[State.current_step]}",  # Dynamic step title
            class_name="text-amber-700",
            font_weight="300",
            margin_bottom="1rem",
            font_size="1.075rem",
            line_height="2.25rem",
            text_align="center",
            as_="h4",
        ),
        
        # Image for the current step
        rx.box(
            rx.image(
                alt=f"Image for Step {State.current_step + 1}",
                src=State.image_url,  # Dynamic image URL
                margin_bottom="2rem",
                border_radius="0.5rem",
                box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
                width="40%",
                align_items="center",
            ),
            display="flex",
            justify_content="center",
            align_items="center",
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