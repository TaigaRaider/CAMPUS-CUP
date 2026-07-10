"""
Sidebar Navigation Widget

Provides the persistent left-hand navigation panel displayed on all
authenticated screens. Contains:
- App branding
- Current user info
- Navigation buttons (Dashboard, Discover, Profile, admin-only items)
- Logout button

The sidebar communicates navigation requests to the parent app via
button press messages handled in app.py.
"""

from __future__ import annotations
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Button
from textual.message import Message
from textual.widget import Widget


class NavButton(Message):
    """Posted when a navigation button is pressed.

    Attributes:
        target: The screen name to navigate to (e.g. 'dashboard', 'discover').
    """
    def __init__(self, target: str) -> None:
        self.target = target
        super().__init__()


class LogoutPressed(Message):
    """Posted when the logout button is pressed."""
    pass


class Sidebar(Widget):
    """Left-hand navigation sidebar.

    Composes user info, nav buttons, and a logout button.
    Emits NavButton / LogoutPressed messages for the app to handle.
    """

    CSS = """  /* Sidebar styling is in theme.tcss */  """

    def __init__(self, username: str, role: str, is_admin: bool = False, **kwargs):
        super().__init__(**kwargs)
        self._username = username
        self._role = role
        self._is_admin = is_admin

    def compose(self) -> ComposeResult:
        with Vertical(id="sidebar"):
            yield Static("CAMPUS CUP", classes="sidebar-title")
            yield Static(self._username, classes="sidebar-user")
            yield Static(self._role, classes="sidebar-role")
            yield Static(classes="sidebar-divider")

            with Vertical(id="nav-buttons"):
                yield Button("  Dashboard", id="nav-dashboard", classes="nav-btn")
                yield Button("  Discover", id="nav-discover", classes="nav-btn")
                yield Button("  Profile", id="nav-profile", classes="nav-btn")
                if self._is_admin:
                    yield Button("  Manage Teams", id="nav-teams", classes="nav-btn")
                    yield Button("  Manage Leagues", id="nav-leagues", classes="nav-btn")

            yield Button("  Logout", id="logout-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Route button presses to appropriate messages."""
        button_id = event.button.id

        if button_id == "logout-btn":
            self.post_message(LogoutPressed())
        elif button_id.startswith("nav-"):
            target = button_id.replace("nav-", "")
            self.post_message(NavButton(target))

    def highlight_button(self, nav_id: str) -> None:
        """Visually highlight the active nav button.

        Args:
            nav_id: The nav target name (e.g. 'dashboard').
        """
        buttons = self.query("Button")
        for btn in buttons:
            if btn.id and btn.id.startswith("nav-"):
                target = btn.id.replace("nav-", "")
                if target == nav_id:
                    btn.add_class("-active")
                else:
                    btn.remove_class("-active")
