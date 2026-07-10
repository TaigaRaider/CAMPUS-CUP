"""
Login Screen

The entry point of the application. Presents a centered login form with:
- Username input
- Password input (masked)
- Login button
- Link to registration screen

On successful authentication, emits a LoginSuccess message that the
main app handles to switch to the dashboard.
"""

from __future__ import annotations
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static, Input, Button, Label
from textual.message import Message
from textual import on


class LoginSuccess(Message):
    """Posted when login is successful."""
    pass


class GoToRegister(Message):
    """Posted when user clicks 'Register here'."""
    pass


class LoginScreen(Screen):
    """Full-screen login form.

    CSS is loaded from theme.tcss (.auth-container, .auth-title, etc.)
    """

    BINDINGS = [
        ("escape", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(classes="auth-container"):
            yield Static("CAMPUS CUP", classes="auth-title")
            yield Static("Intramural Sports League Manager", classes="auth-subtitle")

            yield Label("Username")
            yield Input(placeholder="Enter your username", id="username")

            yield Label("Password")
            yield Input(placeholder="Enter your password", password=True, id="password")

            yield Static("", id="auth-error")

            yield Button("Sign In", id="login-btn", variant="primary")
            yield Button("Don't have an account? Register here", id="goto-register")

    @on(Button.Pressed, "#login-btn")
    def handle_login(self) -> None:
        """Validate credentials via the data store."""
        from store import store

        username = self.query_one("#username", Input).value.strip()
        password = self.query_one("#password", Input).value.strip()

        if not username or not password:
            self.query_one("#auth-error").update("Please fill in all fields")
            return

        user = store.authenticate(username, password)
        if user:
            self.query_one("#auth-error").update("")
            self.post_message(LoginSuccess())
        else:
            self.query_one("#auth-error").update("Invalid username or password")

    @on(Button.Pressed, "#goto-register")
    def handle_goto_register(self) -> None:
        self.post_message(GoToRegister())

    def on_key(self, event) -> None:
        """Allow Enter key to submit the form."""
        if event.key == "enter":
            self.handle_login()

    def action_quit(self) -> None:
        self.app.exit()
