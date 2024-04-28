import datetime
import os
from prompt_toolkit import prompt
from prompt_toolkit.application import get_app
from prompt_toolkit.formatted_text import (
    HTML,
    fragment_list_width,
    merge_formatted_text,
    to_formatted_text,
)


def get_prompt() -> HTML:
    """
    Build the prompt dynamically every time its rendered.
    """
    user_name = os.getlogin()
    cur_path = os.getcwd()
    left_part = HTML(
        "<left-part>"
        f" <username>{user_name}</username> "        
        f"<path>{cur_path}</path>"
        "</left-part>"
    )
    right_part = HTML(
        "<right-part> "                
        " <strong>%s</strong> "
        "</right-part>"
    ) % (datetime.datetime.now().isoformat(),)

    used_width = sum(
        [
            fragment_list_width(to_formatted_text(left_part)),
            fragment_list_width(to_formatted_text(right_part)),
        ]
    )

    total_width = get_app().output.get_size().columns
    padding_size = total_width - used_width

    padding = HTML("<padding>%s</padding>") % (" " * padding_size,)

    return merge_formatted_text([left_part, padding, right_part, "\n", "# "])