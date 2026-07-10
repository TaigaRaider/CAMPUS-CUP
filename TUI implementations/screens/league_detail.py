"""
League Detail Screen

Detailed view for a single league. Shows:
- League name, ID, sport
- Status badge
- Creator info
- Registered teams table
- Scheduled matches table
- Registered match officials

Navigated to from Discover by selecting a league row.
"""

from __future__ import annotations
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Static, DataTable, Button, Header, Footer
from textual.message import Message
from textual import on

from widgets.sidebar import Sidebar, NavButton, LogoutPressed
from classes import League, LeagueStatus


class LeagueDetailScreen(Screen):
    """Detail view for a single league."""

    BINDINGS = [
        ("escape", "pop_screen", "Back"),
    ]

    def __init__(self, league: League, **kwargs):
        super().__init__(**kwargs)
        self._league = league

    def compose(self) -> ComposeResult:
        from store import store
        user = store.current_user
        is_admin = user.is_admin if user else False
        role_str = "Admin" if is_admin else (
            "Player" if hasattr(user, 'position') else "User"
        )
        league = self._league
        status = league.check_league_status()
        status_str = status.value if hasattr(status, 'value') else str(status)

        # Map status to CSS class
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
                yield Static(league.league_name, classes="detail-header")

                # League info card
                with Vertical(classes="detail-card"):
                    with Horizontal(classes="detail-row"):
                        yield Static("League ID: ", classes="detail-label")
                        yield Static(league.league_id, classes="detail-value")
                    with Horizontal(classes="detail-row"):
                        yield Static("Sport: ", classes="detail-label")
                        yield Static(league.sport, classes="detail-value")
                    with Horizontal(classes="detail-row"):
                        yield Static("Status: ", classes="detail-label")
                        yield Static(status_str, classes=f"detail-value {status_css}")
                    with Horizontal(classes="detail-row"):
                        yield Static("Creator: ", classes="detail-label")
                        yield Static(league.creator.user_name, classes="detail-value")
                    with Horizontal(classes="detail-row"):
                        yield Static("Size: ", classes="detail-label")
                        yield Static(f"{len(league.teams)}/{league.league_size} teams", classes="detail-value")

                # Registered teams
                yield Static("Registered Teams", classes="section-header")
                if league.teams:
                    team_table = DataTable()
                    team_table.add_columns("Team Name", "Team ID", "Captain", "Roster")
                    for team in league.teams:
                        team_table.add_row(
                            team.team_name,
                            team.team_id,
                            team.captain.user_name,
                            str(len(team.roster)),
                        )
                    yield team_table
                else:
                    yield Static("  No teams registered yet.", classes="text-muted")

                # Scheduled matches
                yield Static("Matches", classes="section-header")
                if league.matches:
                    match_table = DataTable(id="league-matches-table")
                    match_table.add_columns("Match ID", "Home", "Away", "Score", "Status", "Location")
                    for match in league.matches:
                        ms = match.match_status.value if hasattr(match.match_status, 'value') else str(match.match_status)
                        score = f"{match.home_team_score} - {match.away_team_score}"
                        match_table.add_row(
                            match.match_id,
                            match.home_team.team_name,
                            match.away_team.team_name,
                            score,
                            ms,
                            match.match_location or "TBD",
                        )
                    yield match_table
                else:
                    yield Static("  No matches scheduled yet.", classes="text-muted")

                # Registered officials
                yield Static("Registered Match Officials", classes="section-header")
                if league.registered_match_officials:
                    official_table = DataTable()
                    official_table.add_columns("Name", "Official ID")
                    for official in league.registered_match_officials:
                        official_table.add_row(
                            official.user_name,
                            official.user_id,
                        )
                    yield official_table
                else:
                    yield Static("  No officials registered.", classes="text-muted")

                yield Button("Back to Discover", id="btn-back", variant="primary")

            yield Footer()

    @on(Button.Pressed, "#btn-back")
    def handle_back(self) -> None:
        self.app.pop_screen()

    @on(DataTable.RowSelected, "#league-matches-table")
    def handle_match_selected(self, event: DataTable.RowSelected) -> None:
        from screens.match_detail import MatchDetailScreen
        row_index = event.row_index
        if row_index < len(self._league.matches):
            self.app.push_screen(MatchDetailScreen(self._league.matches[row_index]))

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
