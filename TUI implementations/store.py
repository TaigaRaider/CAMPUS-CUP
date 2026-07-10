"""
CAMPUS-CUP In-Memory Data Store

Centralized data store for the TUI application.
Pre-seeded with demo data for development and testing.

Usage:
    from store import store
    store.current_user  # logged-in user
    store.users         # all registered users
    store.teams         # all teams
    store.leagues       # all leagues
    store.matches       # all matches (shorthand for league matches)
"""

from __future__ import annotations
import sys
import os

# Add parent directory to path so we can import classes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from classes import (
    User, Player, MatchOfficial, Team, League,
    LeagueStatus, MatchStatus
)


class DataStore:
    """Singleton-style data store holding all application state.

    Attributes:
        current_user: The currently authenticated User (None if not logged in).
        users: List of all registered User objects.
        teams: List of all Team objects.
        leagues: List of all League objects.
    """

    def __init__(self):
        self.current_user: User | None = None
        self.users: list[User] = []
        self.teams: list[Team] = []
        self.leagues: list[League] = []

    # ── Authentication ────────────────────────────────────────────

    def authenticate(self, username: str, password: str) -> User | None:
        """Validate credentials and set current_user.

        Returns the matching User on success, None on failure.
        """
        for user in self.users:
            if user.user_name == username and user.password == password:
                self.current_user = user
                return user
        return None

    def register_user(self, username: str, password: str, role: str,
                      position: str = "CF") -> User:
        """Create a new user and add them to the store.

        Args:
            username: Display name for the user.
            password: Plain-text password (stored in-memory for demo).
            role: One of 'player', 'admin', 'official'.
            position: Player position (only used when role == 'player').

        Returns:
            The newly created User object.
        """
        if role == "admin":
            user = User(username, is_admin=True, password=password)
        elif role == "official":
            user = MatchOfficial(username, password=password)
        else:
            user = Player(username, position, password=password)

        self.users.append(user)
        return user

    def logout(self):
        """Clear the current session."""
        self.current_user = None

    def get_user_by_name(self, name: str) -> User | None:
        """Look up a user by their display name."""
        for user in self.users:
            if user.user_name == name:
                return user
        return None

    # ── Team helpers ──────────────────────────────────────────────

    def get_team_by_name(self, name: str) -> Team | None:
        for team in self.teams:
            if team.team_name == name:
                return team
        return None

    def get_teams_for_user(self, user: User) -> list[Team]:
        """Return all teams the given user belongs to (as captain or roster member)."""
        result = []
        for team in self.teams:
            if team.is_captain(user) or team.check_in_team(user):
                result.append(team)
        return result

    # ── League helpers ────────────────────────────────────────────

    def get_league_by_name(self, name: str) -> League | None:
        for league in self.leagues:
            if league.league_name == name:
                return league
        return None

    # ── Match helpers ─────────────────────────────────────────────

    def get_all_matches(self) -> list[League.Match]:
        """Flatten all matches across every league into a single list."""
        all_matches = []
        for league in self.leagues:
            all_matches.extend(league.matches)
        return all_matches

    def get_matches_for_team(self, team: Team) -> list[League.Match]:
        """Return every match involving the given team."""
        result = []
        for league in self.leagues:
            for match in league.matches:
                if match.home_team == team or match.away_team == team:
                    result.append(match)
        return result

    # ── Statistics helpers (used by Dashboard) ────────────────────

    def stats(self) -> dict:
        """Return aggregate statistics for the dashboard."""
        all_matches = self.get_all_matches()
        return {
            "total_users": len(self.users),
            "total_players": sum(1 for u in self.users if isinstance(u, Player)),
            "total_officials": sum(1 for u in self.users if isinstance(u, MatchOfficial)),
            "total_teams": len(self.teams),
            "total_leagues": len(self.leagues),
            "total_matches": len(all_matches),
            "pending_matches": sum(
                1 for m in all_matches if m.match_status == MatchStatus.PENDING
            ),
            "active_matches": sum(
                1 for m in all_matches if m.match_status == MatchStatus.ACTIVE
            ),
            "concluded_matches": sum(
                1 for m in all_matches if m.match_status == MatchStatus.CONCLUDED
            ),
        }


def _seed_demo_data(store: DataStore):
    """Populate the store with demo data for testing the TUI.

    Creates:
        - 2 admin users
        - 4 players (2 per team)
        - 1 match official
        - 2 teams
        - 1 league (REGISTERED status)
        - 2 matches (1 PENDING, 1 ACTIVE)
    """
    # ── Users ─────────────────────────────────────────────────────
    admin1 = User("Admin", is_admin=True, password="admin")
    admin2 = User("Coach Davis", is_admin=True, password="coach")

    player1 = Player("Jay", "RW", password="jay")
    player2 = Player("Jordan", "LW", password="jordan")
    player3 = Player("Jack", "CF", password="jack")
    player4 = Player("Alex Torres", "RB", password="alex")

    official1 = MatchOfficial("Jerry Cooper", password="jerry")

    store.users.extend([admin1, admin2, player1, player2, player3, player4, official1])

    # ── Teams ─────────────────────────────────────────────────────
    team1 = Team("Juggernaut FC", player4)
    team1.roster.extend([player4, player1])

    team2 = Team("Liverpool FC", player3)
    team2.roster.extend([player3, player2])

    store.teams.extend([team1, team2])

    # ── League ────────────────────────────────────────────────────
    # Create league without triggering auto-population
    league = League.__new__(League)
    league.creator = admin1
    league.league_name = "Premier League"
    # Generate ID manually
    league.league_id = "LG-PL-2026-DEMO"
    league.league_size = 2
    league._status = LeagueStatus.REGISTERED
    league.matches = []
    league.registered_match_officials = [official1]
    league.teams = [team1, team2]
    league.sport = "Football"

    store.leagues.append(league)

    # ── Matches ───────────────────────────────────────────────────
    # Match 1: Juggernaut FC vs Liverpool FC (PENDING)
    match1 = League.Match.__new__(League.Match)
    match1.home_team = team1
    match1.away_team = team2
    match1.container_league = league
    match1.match_id = "MCH-PL-JULI-001"
    match1.match_status = MatchStatus.PENDING
    match1.match_location = "University Field A"
    match1.match_datetime = "15-07-2026 18:00"
    match1.start_time = ""
    match1.end_time = ""
    match1.home_team_score = 0
    match1.away_team_score = 0
    match1.match_officials = [official1]

    # Match 2: Liverpool FC vs Juggernaut FC (ACTIVE)
    match2 = League.Match.__new__(League.Match)
    match2.home_team = team2
    match2.away_team = team1
    match2.container_league = league
    match2.match_id = "MCH-PL-LEJU-002"
    match2.match_status = MatchStatus.ACTIVE
    match2.match_location = "University Field B"
    match2.match_datetime = "12-07-2026 15:00"
    match2.start_time = "15:00"
    match2.end_time = ""
    match2.home_team_score = 2
    match2.away_team_score = 1
    match2.match_officials = [official1]

    league.matches.extend([match1, match2])


# ── Module-level singleton ────────────────────────────────────────
store = DataStore()
_seed_demo_data(store)
