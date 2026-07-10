"""
Discover Screen

Browseable interface for exploring all leagues, teams, and matches.
Features a tabbed layout with three views:

- Leagues Tab: Table of all leagues with status, sport, team count
- Teams Tab: Table of all teams with captain, roster size
- Matches Tab: Table of all matches with home/away, score, status

Clicking a row pushes the corresponding detail screen.
"""

from __future__ import annotations
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Static, DataTable, Button, Header, Footer
from textual.message import Message
from textual import on

from widgets.sidebar import Sidebar, NavButton, LogoutPressed


class DiscoverScreen(Screen):
    """Browseable discovery screen with sidebar + tabbed content."""

    BINDINGS = [
        ("escape", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        from store import store
        user = store.current_user
        is_admin = user.is_admin if user else False
        role_str = "Admin" if is_admin else (
            "Player" if hasattr(user, 'position') else "User"
        )

        yield Sidebar(
            username=user.user_name,
            role=role_str,
            is_admin=is_admin,
            id="app-sidebar",
        )

        with Vertical(id="main-content"):
            yield Header()

            with ScrollableContainer():
                yield Static("Discover", classes="dashboard-header")

                # Tab buttons
                with Horizontal(classes="discover-tabs"):
                    yield Button("Leagues", id="tab-leagues", classes="-active")
                    yield Button("Teams", id="tab-teams")
                    yield Button("Matches", id="tab-matches")

                # Leagues table
                yield from self._build_leagues_table(store)
                # Teams table (hidden initially)
                yield from self._build_teams_table(store)
                # Matches table (hidden initially)
                yield from self._build_matches_table(store)

            yield Footer()

    def _build_leagues_table(self, store) -> list:
        table = DataTable(id="leagues-table")
        table.add_columns("League Name", "ID", "Sport", "Teams", "Status", "Creator")
        for league in store.leagues:
            status = league.check_league_status()
            status_str = status.value if hasattr(status, 'value') else str(status)
            table.add_row(
                league.league_name,
                league.league_id,
                league.sport,
                f"{len(league.teams)}/{league.league_size}",
                status_str,
                league.creator.user_name,
            )
        return [table]

    def _build_teams_table(self, store) -> list:
        table = DataTable(id="teams-table")
        table.add_columns("Team Name", "ID", "Captain", "Roster Size")
        for team in store.teams:
            table.add_row(
                team.team_name,
                team.team_id,
                team.captain.user_name,
                str(len(team.roster)),
            )
        table.display = False  # hidden by default
        return [table]

    def _build_matches_table(self, store) -> list:
        table = DataTable(id="discover-matches-table")
        table.add_columns("Match ID", "Home", "Away", "Score", "Status", "Location")
        for match in store.get_all_matches():
            status = match.match_status.value if hasattr(match.match_status, 'value') else str(match.match_status)
            score = f"{match.home_team_score} - {match.away_team_score}"
            table.add_row(
                match.match_id,
                match.home_team.team_name,
                match.away_team.team_name,
                score,
                status,
                match.match_location or "TBD",
            )
        table.display = False  # hidden by default
        return [table]

    @on(Button.Pressed, ".discover-tabs Button")
    def handle_tab_switch(self, event: Button.Pressed) -> None:
        """Switch visible table based on tab selection."""
        tab_id = event.button.id

        # Update button styles
        for btn in self.query(".discover-tabs Button"):
            if btn.id == tab_id:
                btn.add_class("-active")
            else:
                btn.remove_class("-active")

        # Show/hide tables
        self.query_one("#leagues-table").display = (tab_id == "tab-leagues")
        self.query_one("#teams-table").display = (tab_id == "tab-teams")
        self.query_one("#discover-matches-table").display = (tab_id == "tab-matches")

    @on(DataTable.RowSelected, "#leagues-table")
    def handle_league_selected(self, event: DataTable.RowSelected) -> None:
        from store import store
        from screens.league_detail import LeagueDetailScreen
        row_index = event.row_index
        if row_index < len(store.leagues):
            self.app.push_screen(LeagueDetailScreen(store.leagues[row_index]))

    @on(DataTable.RowSelected, "#teams-table")
    def handle_team_selected(self, event: DataTable.RowSelected) -> None:
        from store import store
        from screens.team_detail import TeamDetailScreen
        row_index = event.row_index
        if row_index < len(store.teams):
            self.app.push_screen(TeamDetailScreen(store.teams[row_index]))

    @on(DataTable.RowSelected, "#discover-matches-table")
    def handle_match_selected(self, event: DataTable.RowSelected) -> None:
        from store import store
        from screens.match_detail import MatchDetailScreen
        row_index = event.row_index
        all_matches = store.get_all_matches()
        if row_index < len(all_matches):
            self.app.push_screen(MatchDetailScreen(all_matches[row_index]))

    @on(NavButton)
    def handle_nav(self, event: NavButton) -> None:
        self.app.switch_screen(event.target)

    @on(LogoutPressed)
    def handle_logout(self) -> None:
        from store import store
        store.logout()
        self.app.switch_screen("login")

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.app.exit()

    def action_quit(self) -> None:
        self.app.exit()
