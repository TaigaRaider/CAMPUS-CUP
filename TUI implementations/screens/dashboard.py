"""
Dashboard Screen

The main landing screen after login. Adapts its layout based on the
current user's role:

Admin Dashboard:
- Aggregate stats row (users, teams, leagues, matches)
- Pending matches count
- Quick actions (links to create/manage)

Player / User Dashboard:
- My Teams section
- My Upcoming Matches
- Recent Results

Both variants show a greeting and the user's role badge.
"""

from __future__ import annotations
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Static, DataTable, Button, Header, Footer, Label
from textual.message import Message
from textual import on

from widgets.sidebar import Sidebar, NavButton, LogoutPressed
from widgets.stat_card import StatCard


class DashboardScreen(Screen):
    """Main dashboard screen with sidebar + content layout."""

    BINDINGS = [
        ("escape", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        from store import store
        user = store.current_user
        stats = store.stats()

        is_admin = user.is_admin if user else False
        role_str = "Admin" if is_admin else (
            "Player" if hasattr(user, 'position') else "User"
        )

        # Sidebar
        yield Sidebar(
            username=user.user_name if user else "Guest",
            role=role_str,
            is_admin=is_admin,
            id="app-sidebar",
        )

        # Main content area
        with Vertical(id="main-content"):
            yield Header()

            with ScrollableContainer():
                yield Static(f"Welcome back, {user.user_name}!", classes="dashboard-header")

                # Stats row
                with Horizontal(classes="stats-row"):
                    yield StatCard(str(stats["total_users"]), "Total Users", variant="primary")
                    yield StatCard(str(stats["total_teams"]), "Total Teams", variant="success")
                    yield StatCard(str(stats["total_leagues"]), "Total Leagues", variant="primary")
                    yield StatCard(str(stats["total_matches"]), "Total Matches", variant="success")

                # Pending / Active matches row
                with Horizontal(classes="stats-row"):
                    yield StatCard(str(stats["pending_matches"]), "Pending Matches")
                    yield StatCard(str(stats["active_matches"]), "Active Matches", variant="success")
                    yield StatCard(str(stats["concluded_matches"]), "Concluded Matches")

                if is_admin:
                    yield Static("Quick Actions", classes="section-header")
                    with Horizontal():
                        yield Button("Create League", id="btn-create-league", variant="primary")
                        yield Button("Manage Teams", id="btn-manage-teams", variant="success")

                # Recent matches table
                yield Static("Recent Matches", classes="section-header")
                table = DataTable(id="matches-table")
                table.add_columns("Match ID", "Home", "Away", "Score", "Status", "League")
                for match in store.get_all_matches()[-5:]:  # last 5 matches
                    status = match.match_status.value if hasattr(match.match_status, 'value') else str(match.match_status)
                    score = f"{match.home_team_score} - {match.away_team_score}"
                    table.add_row(
                        match.match_id,
                        match.home_team.team_name,
                        match.away_team.team_name,
                        score,
                        status,
                        match.container_league.league_name,
                    )
                yield table

                # My teams (for non-admin users)
                if not is_admin:
                    yield Static("My Teams", classes="section-header")
                    my_teams = store.get_teams_for_user(user)
                    if my_teams:
                        team_table = DataTable(id="my-teams-table")
                        team_table.add_columns("Team", "ID", "Captain", "Roster Size")
                        for team in my_teams:
                            team_table.add_row(
                                team.team_name,
                                team.team_id,
                                team.captain.user_name,
                                str(len(team.roster)),
                            )
                        yield team_table
                    else:
                        yield Static("  No team affiliations yet.", classes="text-muted")

            yield Footer()

    @on(DataTable.RowSelected, "#matches-table")
    def handle_match_selected(self, event: DataTable.RowSelected) -> None:
        """Navigate to match detail when a row is clicked."""
        from store import store
        from screens.match_detail import MatchDetailScreen
        row_index = event.row_index
        all_matches = store.get_all_matches()[-5:]
        if row_index < len(all_matches):
            match = all_matches[row_index]
            self.app.push_screen(MatchDetailScreen(match))

    @on(Button.Pressed, "#btn-create-league")
    def handle_create_league(self) -> None:
        self.app.switch_screen("discover")

    @on(Button.Pressed, "#btn-manage-teams")
    def handle_manage_teams(self) -> None:
        self.app.switch_screen("discover")

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
