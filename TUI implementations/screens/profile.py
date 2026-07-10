"""
Profile Screen

Displays the current user's profile information:
- Name, User ID, Role badge
- Position (for players)
- Team affiliations
- Recent match history
"""

from __future__ import annotations
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Static, DataTable, Header, Footer
from textual.message import Message
from textual import on

from widgets.sidebar import Sidebar, NavButton, LogoutPressed
from classes import Player, MatchOfficial


class ProfileScreen(Screen):
    """User profile screen with sidebar + content layout."""

    BINDINGS = [
        ("escape", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        from store import store
        user = store.current_user
        if not user:
            return

        is_admin = user.is_admin
        role_str = "Admin" if is_admin else (
            "Player" if isinstance(user, Player) else (
                "Match Official" if isinstance(user, MatchOfficial) else "User"
            )
        )

        # Badge class
        if is_admin:
            badge_cls = "badge badge-admin"
        elif isinstance(user, Player):
            badge_cls = "badge badge-player"
        else:
            badge_cls = "badge badge-official"

        yield Sidebar(
            username=user.user_name,
            role=role_str,
            is_admin=is_admin,
            id="app-sidebar",
        )

        with Vertical(id="main-content"):
            yield Header()

            with ScrollableContainer():
                yield Static("My Profile", classes="dashboard-header")

                # Profile card
                with Vertical(classes="profile-card"):
                    yield Static(user.user_name, classes="profile-name")
                    yield Horizontal(
                        Static(f"ID: {user.user_id}", classes="profile-id"),
                        Static(role_str, classes=badge_cls),
                    )
                    if isinstance(user, Player):
                        yield Horizontal(
                            Static("Position: ", classes="profile-field-label"),
                            Static(user.position, classes="profile-field-value"),
                        )

                # Team affiliations
                yield Static("My Teams", classes="section-header")
                my_teams = store.get_teams_for_user(user)
                if my_teams:
                    team_table = DataTable()
                    team_table.add_columns("Team Name", "Team ID", "Captain", "Role", "Roster Size")
                    for team in my_teams:
                        role_in_team = "Captain" if team.is_captain(user) else "Player"
                        team_table.add_row(
                            team.team_name,
                            team.team_id,
                            team.captain.user_name,
                            role_in_team,
                            str(len(team.roster)),
                        )
                    yield team_table
                else:
                    yield Static("  Not currently on any team.", classes="text-muted")

                # Match history
                yield Static("Match History", classes="section-header")
                if isinstance(user, Player):
                    user_teams = store.get_teams_for_user(user)
                    all_relevant = []
                    for team in user_teams:
                        all_relevant.extend(store.get_matches_for_team(team))

                    if all_relevant:
                        match_table = DataTable()
                        match_table.add_columns("Match ID", "Opponent", "Score", "Status", "Location")
                        for match in all_relevant:
                            opponent = match.away_team if match.home_team in user_teams else match.home_team
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
                        yield Static("  No match history yet.", classes="text-muted")
                else:
                    # For admins/officials, show all matches
                    all_matches = store.get_all_matches()
                    if all_matches:
                        match_table = DataTable()
                        match_table.add_columns("Match ID", "Home", "Away", "Score", "Status")
                        for match in all_matches:
                            score = f"{match.home_team_score} - {match.away_team_score}"
                            status = match.match_status.value if hasattr(match.match_status, 'value') else str(match.match_status)
                            match_table.add_row(
                                match.match_id,
                                match.home_team.team_name,
                                match.away_team.team_name,
                                score,
                                status,
                            )
                        yield match_table
                    else:
                        yield Static("  No matches in the system.", classes="text-muted")

            yield Footer()

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
