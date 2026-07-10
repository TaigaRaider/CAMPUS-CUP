"""
CAMPUS-CUP Terminal UI Application

Main entry point for the Textual-based TUI. Wires together all screens,
handles screen navigation, authentication flow, and loads the theme CSS.

Usage:
    cd "TUI implementations"
    python app.py

Login with any of the pre-seeded demo accounts:
    Admin:       username="Admin"        password="admin"
    Coach:       username="Coach Davis"  password="coach"
    Player:      username="Jay"          password="jay"
    Player:      username="Jordan"       password="jordan"
    Player:      username="Jack"         password="jack"
    Player:      username="Alex Torres"  password="alex"
    Official:    username="Jerry Cooper" password="jerry"

Screen Flow:
    Login ──► Dashboard ──┬──► Discover ──┬──► Team Detail
                         │               ├──► League Detail
                         │               └──► Match Detail
                         ├──► Profile
                         └──► Logout ──► Login

    Login ──► Register ──► Login

Architecture:
    - screens/  : Textual Screen subclasses (one per page)
    - widgets/  : Reusable UI components (Sidebar, StatCard)
    - store.py  : In-memory data store with pre-seeded demo data
    - classes.py: Data model classes (cloned and adapted from root)
    - styles/   : Textual CSS theme (black/blue/green palette)
"""

from __future__ import annotations
import sys
import os

# Ensure we can import sibling modules when run from this directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual import on

from screens.login import LoginScreen, LoginSuccess, GoToRegister
from screens.register import RegisterScreen, RegisterSuccess, GoToLogin
from screens.dashboard import DashboardScreen
from screens.profile import ProfileScreen
from screens.discover import DiscoverScreen
from screens.team_detail import TeamDetailScreen
from screens.league_detail import LeagueDetailScreen
from screens.match_detail import MatchDetailScreen


class CampusCupApp(App):
    """CAMPUS-CUP Intramural Sports League Manager — Terminal UI.

    This is the root Textual application. It manages:
    - Screen registration and lifecycle
    - Screen transitions (switch_screen / push_screen / pop_screen)
    - CSS theme loading
    - Authentication flow (login → register → login)

    Screens that don't require constructor arguments are registered
    via the SCREENS dict and referenced by name (e.g. "login").
    Parameterized screens (detail views) are pushed as instances.
    """

    # Load the theme CSS from the styles directory
    CSS_PATH = os.path.join("styles", "theme.tcss")

    # App title shown in terminal title bar
    TITLE = "CAMPUS-CUP — Intramural Sports League Manager"

    # Register screens that don't require constructor arguments.
    # Screens needing data (team_detail, league_detail, match_detail)
    # are pushed as instances from the screens that reference them.
    SCREENS = {
        "login": LoginScreen,
        "register": RegisterScreen,
        "dashboard": DashboardScreen,
        "profile": ProfileScreen,
        "discover": DiscoverScreen,
    }

    def on_mount(self) -> None:
        """Called when the app starts. Push the login screen."""
        self.push_screen("login")

    def compose(self) -> ComposeResult:
        """App root composition — screens are pushed/popped dynamically."""
        return []

    # ── Screen message handlers ───────────────────────────────────

    @on(LoginSuccess)
    def handle_login_success(self) -> None:
        """Transition from login to dashboard."""
        self.switch_screen("dashboard")

    @on(GoToRegister)
    def handle_goto_register(self) -> None:
        """Transition from login to registration."""
        self.switch_screen("register")

    @on(RegisterSuccess)
    def handle_register_success(self) -> None:
        """Transition from registration back to login."""
        self.switch_screen("login")

    @on(GoToLogin)
    def handle_goto_login(self) -> None:
        """Transition from registration back to login."""
        self.switch_screen("login")


def main():
    """Launch the CAMPUS-CUP TUI application."""
    app = CampusCupApp()
    app.run()


if __name__ == "__main__":
    main()
