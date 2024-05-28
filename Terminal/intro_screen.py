from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Box, Frame, Label
from prompt_toolkit import HTML
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.keys import Keys

msg = """

        <b><green>Welcome to the Terminal Quiz App!</green></b>

        This app is designed to help you learn and master the GNU/Linux terminal. 
        Using the command line interface (CLI) offers numerous benefits, such as:

        - Faster and more efficient file and folder management.
        - Advanced control over system operations and processes.
        - Enhanced security and network management capabilities.
        - Access to powerful CLI tools that are not available in graphical user interfaces (GUIs).
        - Essential skills for server management, where a GUI may not be available.

        The terminal is an indispensable tool for any Linux user, 
        and proficiency in its use is crucial. 
        This quiz app will guide you through everything you need to know to become proficient in the Linux terminal,
        ensuring you are well above average in your skills.

        <yellow>Instructions</yellow>

        1. <b>Interact with the App</b>: You will be provided with questions and will interact directly with the app to solve them.
        2. <b>Submit Your Answer</b>: Use `Ctrl + S` to submit your answer.
        3. <b>Get Help</b>: Use flags like `learncli --help` to see additional instructions and tips.

        Best of luck! Enjoy your learning journey with the Terminal Quiz App.

        <b><blue>Press ANY key to start</blue></b>

"""

root_container = Box(
    padding_left=D(max=30, min=30),
    body=Frame(
        body=Label(
            text=HTML(msg),
        )
    )
)

layout = Layout(container=root_container)

kb = KeyBindings()


@kb.add(Keys.Any)
def _(event):
    event.app.exit()


application = Application(layout=layout, key_bindings=kb, full_screen=True)


def introduce():
    application.run()
