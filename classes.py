from __future__ import annotations
import time

from rich.progress import track
from rich.prompt import Prompt

from enum import StrEnum

class LeagueStatus(StrEnum):
    REGISTERING = "REGISTERING"
    REGISTERED = "REGISTERED"
    ACTIVE = "ACTIVE"
    CONCLUDED = "CONCLUDED"

class MatchStatus(StrEnum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    CONCLUDED = "CONCLUDED"


class User:
    def __init__(self, user_name: str, is_admin: bool):
        self.user_name = user_name
        self.is_admin = is_admin

    def __str__(self):
        return self.user_name


class Player(User):
    def __init__(self, player_name: str, position: str, is_admin):
        super().__init__(player_name, is_admin)
        self.position = position
        self._teams: list[Team] = []

    def __str__(self):
        return f"{self.user_name}"

    def __repr__(self):
        return f"Player name:{self.user_name}\n Position: {self.user_name}\n"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return self.user_name == other.user_name and self.position == other.position



class MatchOfficial(User):
    def __init__(self, match_official_name: str):
        super().__init__(match_official_name, is_admin = False)

    def __str__(self):
        return f"Match official name:{self.user_name}"

    def __eq__(self, other)-> bool:
        if not isinstance(other, MatchOfficial):
            return False
        return self.user_name == other.user_name

class Team:
    def __init__(self, team_name: str):
        self.team_name = team_name
        self.roster: list[Player] = []
        self.captain: Player | None = None

    def __str__(self):
        return f"Team name: {self.team_name}"

    def __repr__(self):
        return f"Team name: {self.team_name}\n Players: {self.roster}"

    def __hash__(self) -> int:
        return hash(self.team_name)

    def __len__(self) -> int:
        return len(self.roster)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Team):
            return False
        return self.team_name == other.team_name

    def is_captain(self, player: Player)-> bool:
        """Helper method to encapsulate captaincy check"""
        return player == self.captain

    def check_in_team(self, player: Player) -> bool | None:
        """Helper method to encapsulate membership check"""
        for team_member in self.roster:
            if player == team_member:
                return True

        return None

    def find_in_team(self, player: Player) -> int | None:
        """Helper method to encapsulate membership data lookup"""
        for team_member in self.roster:
            if player == team_member:
                return self.roster.index(player)
        return None

    def add_player(self, actor: User | Player, player: Player):
        """Guarded method: Only Captains and Administrators can add players"""
        if not self.is_captain(actor) and not check_admin(actor):
            raise PermissionError(f"You do not have permission to add players")

        if not self.check_in_team(player):
            self.roster.append(player)
            return f"Player was Successfully added"
        else:
            raise ValueError(f"{player} is already in the team!")

    def remove_player(self,actor: User | Player, player: Player) -> None:
        """Guarded method: Only Captains can remove players"""
        if not self.is_captain(actor) and not check_admin(actor):
            raise PermissionError(f"You do not have permission to remove players")

        for team_member in self.roster:
            if player == team_member:
                self.roster.remove(player)
                break

    def sys_fetch_squad(self):
        return list(self.roster)

    def fetch_squad(self):
        for player in self.roster:
            formatted_player = (f"{self.roster.index(player) + 1}. |\tName: {player.user_name}\t|\n"
                                f"   |\tPosition: {player.position}\t|")
            print(formatted_player)
        print(f"\nSquad Fetch Complete!")

    def appoint_team_captain(self, actor: User | Player, target_player: Player):
        """Guarded method: Only Captains or Administrators can change team Settings"""
        if not self.is_captain(actor) and not check_admin(actor):
            raise PermissionError(f"You do not have Permission to appoint captains!")

        if not self.check_in_team(target_player):
            raise ValueError(f"Target Player {target_player} Not in Roster!")
        else:
            self.captain = target_player
            return f"Successful"


    class Formation:
        def __init__(self, formation_name: str, use_case: str):
            self.formation_name = formation_name
            self.use_case = use_case

    class PracticeSession:
        def __init__(self, session_name: str, session_date: str, session_time: str):
            self.session_name = session_name
            self.session_date = session_date
            self.session_time = session_time


class League:
    def __init__(self, league_name: str, league_size: int, sport: str):
        self.league_name = league_name
        self.league_size = league_size
        self.status = LeagueStatus.REGISTERING
        self.matches: list[League.Match] = []
        self.registered_match_officials : list[MatchOfficial] = [MatchOfficial("Jerry Cooper")]
        self.teams: list[Team] = []
        self.sport = sport.capitalize()


    def populate_league(self,actor: User, deficit: int):
        """Guarded method: Only Administrators can manage League states"""
        if not check_admin(actor):
            raise PermissionError(f"Only Administrators can manage league states")
        for i in range(deficit):
            team_name = Prompt.ask(f"Enter the name of the team #{i+1}")
            team = Team(team_name)
            self.teams.append(team)

    def population_check(self, actor: User)-> bool:
        """Helper method to encapsulate population check"""
        if len(self.teams) < self.league_size:
            if len(self.teams) == 0:
                self.populate_league(actor, self.league_size)
                return True
            else:
                self.populate_league(actor, self.league_size - len(self.teams))
                return True
        elif len(self.teams) == self.league_size:
            return True

        return False

    def fetchOfficials(self):
        return self.registered_match_officials

    def update_league_status(self, actor: User, new_status: LeagueStatus):
        """Guarded method: To prevent regular users from changing League States"""
        if not check_admin(actor):
            raise PermissionError(f"Only Administrators can modify League State!")

        if not isinstance(new_status, LeagueStatus):
            raise TypeError(f"Expected Type LeagueStatus got type {type(new_status)}")


    def is_registered_official(self, official: MatchOfficial)-> bool:
            """
            Helper method: To encapsulate check for REGISTERED Match Officials
            Note: ONLY match officials that have been explicitly included in a League's Match Official list are deemed REGISTERED!
            """
            if official in self.fetchOfficials():
                return True
            else:
                return False

    class Match:
        match_ids: list[int] = []

        def __init__(self, home_team: Team, away_team: Team, container_league: League):
            self.home_team = home_team
            self.away_team = away_team
            self.container_league = container_league
            self.match_id = self.generate_match_id()

            self.match_status = MatchStatus.PENDING
            self.match_location = ""
            self.match_datetime = ""
            self.start_time = ""
            self.end_time = ""

            self.home_team_score = 0
            self.away_team_score = 0
            self.match_officials: list[MatchOfficial] = []

        def __str__(self):
            return f"{self.home_team} vs {self.away_team}"

        def __repr__(self):
            return f"Team 1:{self.home_team}\nTeam 2:{self.away_team}\nStatus:{self.match_status}"

        def start_match(self):
            pass

        def generate_match_id(self) -> str:
            unique_match_index: int = len(League.Match.match_ids) + 1
            match_team_acr: str = self.home_team.team_name[0] + self.away_team.team_name[0]
            match_league_acr: str = self.container_league.league_name.strip().replace(" ", "").replace("eague", "")

            match_id = f"{match_team_acr}{match_league_acr}{unique_match_index:2}"
            return match_id

            # unique_match_index: str = str(len(League.Match.match_ids) + 1)
            # match_team_acr: str = str(self.home_team.__hash__()) + str(self.away_team.__hash__())
            # match_league_acr: str = self.league_name
            #
            # match_id= f"{match_team_acr[1:5]}{match_league_acr.strip()}{unique_match_index[0:2]}"
            # return match_id


        def appoint_officials(self, actor: User, *args: MatchOfficial):
            """Guarded method: Only Registered Administrators can appoint Match Officials """
            if not check_admin(actor):
                raise PermissionError(f"Only Registered Administrators can appoint Match Officials")

            for official in args:
                if not self.container_league.is_registered_official(official):
                    raise ValueError(f"{official.user_name} is not a registered Official")

                self.match_officials.append(official)


        def end_match(self):
            pass

        def pause_match(self):
            pass

        def resume_match(self):
            pass

        def extend_match(self):
            pass

        def report_match(self):
            pass

        def reschedule_match(self, new_time: str):
            """Query schedule and check if a match is holding at the newly selected date time and venue"""

            if self.match_status != "COMPLETED":
                new_time = Prompt.ask(f"Enter a new match date and time in the order DD-MM-YYYY HH:MM" )
                self.match_datetime = new_time

            """if none, assign match to new date"""


    class RuleSet:
        ruleSet: dict = {
            "WIN": "",
            "DRAW": "",
            "LOSS": "",
            "OFFENCE": ""
        }

        temp_ruleSet = ruleSet.copy()

        def __init__(self, ruleset_name: str):
            self.ruleset_name = ruleset_name

        def update_ruleset(self):
            for key, value in track(self.ruleSet.items(), description="Updating Ruleset..."):
                value = Prompt.ask(f"What should be happen after a {key}")
                self.ruleSet[key] = value

        def validate_ruleset(self):
            print(self.ruleSet)
            confirmation = Prompt.ask("Is this your desired ruleset(True/False)? ")

            match confirmation:
                case ("True"):
                    self.temp_ruleSet = {}
                    print(f"Ruleset Successfully Updated!")

                case ("False"):
                    self.ruleSet = self.temp_ruleSet.copy()
                    print("Reverting ruleset...")
                    time.sleep(0.5)
                    print(f"{self.ruleSet}\nUpdate Successfully Reverted!")

                case _:
                    print(f"Invalid Input")


def check_admin(actor)-> bool :
    """Helper method: To encapsulate Admin check"""
    return actor.is_admin