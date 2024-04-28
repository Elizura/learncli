from injector import inject
from dataclasses import dataclass
from prompt_toolkit.styles import Style

@inject
@dataclass
class StyleProvider:

    def get_fancy_zhs_style(self):
        style = Style.from_dict(
            {
                "username": "#aaaaaa italic",
                "path": "#ffffff bold",
                "branch": "bg:#666666",
                "branch exclamation-mark": "#ff0000",
                "env": "bg:#666666",
                "left-part": "bg:#444444",
                "right-part": "bg:#444444",
                "padding": "bg:#444444",
            }
        )

        return style