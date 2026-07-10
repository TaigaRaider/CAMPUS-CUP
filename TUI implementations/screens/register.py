"""
Register Screen

Allows new users to create an account. Fields:
- Username
- Password
- Role selector (Player / Admin / Official)
- Position field (only visible when role is Player)

On successful registration, emits RegisterSuccess to return to login.
"""

from __future__ import annotations
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static, Input, Button, Label, Select, Header, Footer
from textual.message import Message
from textual import on


class RegisterSuccess(Message):
    """Posted when registration completes successfully."""
    pass


class GoToLogin(Message):
    """Posted when user clicks 'Back to login'."""
    pass


class RegisterScreen(Screen):
    """Full-screen registration form."""

    BINDINGS = [
        ("escape", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with Vertical(classes="auth-container"):
            yield Static("CREATE ACCOUNT", classes="auth-title")
            yield Static("Join the Intramural Sports League", classes="auth-subtitle")

            yield Label("Username")
            yield Input(placeholder="Choose a username", id="reg-username")

            yield Label("Password")
            yield Input(placeholder="Choose a password", password=True, id="reg-password")

            yield Label("Role")
            yield Select(
                [(  "Player", "player"),
                 (  "Admin", "admin"),
                 (  "Match Official", "official")],
                id="reg-role",
                prompt="Select your role...",
            )

            yield Label("Position (Players only)")
            yield Input(placeholder="e.g. RW, LW, CF, RB", id="reg-position")

            yield Static("", id="reg-error")
            yield Static("", id="reg-success")

            yield Button("Create Account", id="register-btn", variant="success")
            yield Button("Already have an account? Sign in", id="goto-login")

    @on(Button.Pressed, "#register-btn")
    def handle_register(self) -> None:
        """Validate inputs and register the user."""
        from store import store

        username = self.query_one("#reg-username", Input).value.strip()
        password = self.query_one("#reg-password", Input).value.strip()
        role_val = self.query_one("#reg-role", Select).value
        position = self.query_one("#reg-position", Input).value.strip()

        error_label = self.query_one("#reg-error")
        success_label = self.query_one("#reg-success")
        error_label.update("")
        success_label.update("")

        if not username or not password:
            error_label.update("Username and password are required")
            return

        if role_val is Select.BLANK:
            error_label.update("Please select a role")
            return

        if role_val == "player" and not position:
            error_label.update("Position is required for players")
            return

        # Check for duplicate username
        if store.get_user_by_name(username):
            error_label.update("Username already taken")
            return

        store.register_user(username, password, role_val, position)
        success_label.update("Account created! Redirecting to login...")
        self.set_timer(1.5, lambda: self.post_message(RegisterSuccess()))

    @on(Button.Pressed, "#goto-login")
    def handle_goto_login(self) -> None:
        self.post_message(GoToLogin())

    def on_key(self, event) -> None:
        if event.key == "enter":
            self.handle_register()

    def action_quit(self) -> None:
        self.app.exit()
