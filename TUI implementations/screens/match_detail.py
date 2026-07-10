"""
Match Detail Screen

Detailed view for a single match. Shows:
- Match ID
- Home team vs Away team with score display
- Match status badge
- Location and datetime
- Assigned officials
- League association

Navigated to from Discover, Dashboard, or League Detail.
"""

from __future__ import annotations
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Static, DataTable, Button, Header, Footer
from textual.message import Message
from textual import on

from widgets.sidebar import Sidebar, NavButton, LogoutPressed
from classes import League


class MatchDetailScreen(Screen):
    """Detail view for a single match."""

    BINDINGS = [
        ("escape", "pop_screen", "Back"),
    ]

    def __init__(self, match: League.Match, **kwargs):
        super().__init__(**kwargs)
        self._match = match

    def compose(self) -> ComposeResult:
        from store import store
        user = store.current_user
        is_admin = user.is_admin if user else False
        role_str = "Admin" if is_admin else (
            "Player" if hasattr(user, 'position') else "User"
        )
        match = self._match
        status = match.match_status
        status_str = status.value if hasattr(status, 'value') else str(status)
        status_css = f"status-{status_str.lower()}"

        yield Sidebar(
            username=user.user_name,
            role=role_str,
            is_admin=is_admin,
            id="app-sidebar",
        )

        with Vertical(id="main-content"):
            yield Header()

            with ScrollableContainer():
                yield Static("Match Details", classes="detail-header")

                # Score display
                score_text = f"  {match.home_team.team_name}  {match.home_team_score} : {match.away_team_score}  {match.away_team.team_name}  "
                yield Static(score_text, classes="score-display")

                # Match info card
                with Vertical(classes="detail-card"):
                    with Horizontal(classes="detail-row"):
                        yield Static("Match ID: ", classes="detail-label")
                        yield Static(match.match_id, classes="detail-value")
                    with Horizontal(classes="detail-row"):
                        yield Static("Status: ", classes="detail-label")
                        yield Static(status_str, classes=f"detail-value {status_css}")
                    with Horizontal(classes="detail-row"):
                        yield Static("Home Team: ", classes="detail-label")
                        yield Static(match.home_team.team_name, classes="detail-value")
                    with Horizontal(classes="detail-row"):
                        yield Static("Away Team: ", classes="detail-label")
                        yield Static(match.away_team.team_name, classes="detail-value")
                    with Horizontal(classes="detail-row"):
                        yield Static("Location: ", classes="detail-label")
                        yield Static(match.match_location or "Not set", classes="detail-value")
                    with Horizontal(classes="detail-row"):
                        yield Static("Date/Time: ", classes="detail-label")
                        yield Static(match.match_datetime or "Not set", classes="detail-value")
                    with Horizontal(classes="detail-row"):
                        yield Static("League: ", classes="detail-label")
                        yield Static(match.container_league.league_name, classes="detail-value")

                # Officials
                yield Static("Match Officials", classes="section-header")
                if match.match_officials:
                    official_table = DataTable()
                    official_table.add_columns("Name", "Official ID")
                    for official in match.match_officials:
                        official_table.add_row(
                            official.user_name,
                            official.user_id,
                        )
                    yield official_table
                else:
                    yield Static("  No officials assigned.", classes="text-muted")

                # Team rosters side by side
                yield Static("Team Rosters", classes="section-header")
                with Horizontal():
                    with Vertical(classes="detail-card"):
                        yield Static(match.home_team.team_name, classes="text-blue text-bold")
                        for player in match.home_team.roster:
                            role = " (C)" if match.home_team.is_captain(player) else ""
                            yield Static(f"  {player.user_name} - {player.position}{role}")
                    with Vertical(classes="detail-card"):
                        yield Static(match.away_team.team_name, classes="text-blue text-bold")
                        for player in match.away_team.roster:
                            role = " (C)" if match.away_team.is_captain(player) else ""
                            yield Static(f"  {player.user_name} - {player.position}{role}")

                yield Button("Back", id="btn-back", variant="primary")

            yield Footer()

    @on(Button.Pressed, "#btn-back")
    def handle_back(self) -> None:
        self.app.pop_screen()

    @on(NavButton)
    def handle_nav(self, event: NavButton) -> None:
        self.app.switch_screen(event.target)

    @on(LogoutPressed)
    def handle_logout(self) -> None:
        from store import store
        store.logout()
        self.app.switch_screen("login")

    def action_pop_screen(self) -> None:
        self.app.pop_screen()
