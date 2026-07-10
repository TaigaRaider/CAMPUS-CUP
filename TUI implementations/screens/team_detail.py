"""
Team Detail Screen

Detailed view for a single team. Shows:
- Team name and ID
- Captain info
- Full roster table (name, position, player ID)
- Formations (if any)
- Practice sessions (if any)

Navigated to from Discover or Dashboard by selecting a team row.
"""

from __future__ import annotations
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Static, DataTable, Button, Header, Footer
from textual.message import Message
from textual import on

from widgets.sidebar import Sidebar, NavButton, LogoutPressed
from classes import Team


class TeamDetailScreen(Screen):
    """Detail view for a single team."""

    BINDINGS = [
        ("escape", "pop_screen", "Back"),
    ]

    def __init__(self, team: Team, **kwargs):
        super().__init__(**kwargs)
        self._team = team

    def compose(self) -> ComposeResult:
        from store import store
        user = store.current_user
        is_admin = user.is_admin if user else False
        role_str = "Admin" if is_admin else (
            "Player" if hasattr(user, 'position') else "User"
        )
        team = self._team

        yield Sidebar(
            username=user.user_name,
            role=role_str,
            is_admin=is_admin,
            id="app-sidebar",
        )

        with Vertical(id="main-content"):
            yield Header()

            with ScrollableContainer():
                yield Static(team.team_name, classes="detail-header")
                yield Static(f"Team ID: {team.team_id}", classes="detail-subheader")

                # Team info card
                with Vertical(classes="detail-card"):
                    with Horizontal(classes="detail-row"):
                        yield Static("Captain: ", classes="detail-label")
                        yield Static(team.captain.user_name, classes="detail-value")
                    with Horizontal(classes="detail-row"):
                        yield Static("Roster Size: ", classes="detail-label")
                        yield Static(str(len(team.roster)), classes="detail-value")
                    with Horizontal(classes="detail-row"):
                        yield Static("Captain Position: ", classes="detail-label")
                        yield Static(team.captain.position, classes="detail-value")

                # Roster table
                yield Static("Roster", classes="section-header")
                roster_table = DataTable(id="roster-table")
                roster_table.add_columns("#", "Player Name", "Position", "Player ID", "Role")
                for idx, player in enumerate(team.roster, 1):
                    role_in_team = "Captain" if team.is_captain(player) else "Player"
                    roster_table.add_row(
                        str(idx),
                        player.user_name,
                        player.position,
                        player.user_id,
                        role_in_team,
                    )
                yield roster_table

                # Match history for this team
                yield Static("Match History", classes="section-header")
                team_matches = store.get_matches_for_team(team)
                if team_matches:
                    match_table = DataTable()
                    match_table.add_columns("Match ID", "Opponent", "Score", "Status", "Location")
                    for match in team_matches:
                        opponent = match.away_team if match.home_team == team else match.home_team
                        score = f"{match.home_team_score} - {match.away_team_score}"
                        status = match.match_status.value if hasattr(match.match_status, 'value') else str(match.match_status)
                        match_table.add_row(
                            match.match_id,
                            opponent.team_name,
                            score,
                            status,
                            match.match_location or "TBD",
                        )
                    yield match_table
                else:
                    yield Static("  No matches played yet.", classes="text-muted")

                # Back button
                yield Button("Back to Discover", id="btn-back", variant="primary")

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
