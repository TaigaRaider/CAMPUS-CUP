from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, RadioButton, Static, Label


class Campus(App):
    CSS = """
    Label, Static {
        margin: 1;
        
        background: pink;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Static("This is a static text")
        yield Label("This is a label")
        yield Button("Click me!")
        yield RadioButton("Radio")

if __name__ == "__main__":
    campus = Campus()
    campus.run()
