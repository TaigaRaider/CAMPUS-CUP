"""
CAMPUS-CUP TUI Screens Package

All screen modules for the Terminal UI application.
"""

from screens.login import LoginScreen
from screens.register import RegisterScreen
from screens.dashboard import DashboardScreen
from screens.profile import ProfileScreen
from screens.discover import DiscoverScreen
from screens.team_detail import TeamDetailScreen
from screens.league_detail import LeagueDetailScreen
from screens.match_detail import MatchDetailScreen

__all__ = [
    "LoginScreen",
    "RegisterScreen",
    "DashboardScreen",
    "ProfileScreen",
    "DiscoverScreen",
    "TeamDetailScreen",
    "LeagueDetailScreen",
    "MatchDetailScreen",
]
