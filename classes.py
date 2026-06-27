from __future__ import annotations
import time

import random
import string
import os

from rich.progress import track
from rich.prompt import Prompt
from copy import deepcopy
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


def check_id_exists(target_id: str, filename: str) -> bool:
    """Helper method: Checks if a similar ID exists within the target ID file in the directory."""
    file_path = os.path.join("ids", filename)
    if not os.path.exists(file_path):
        return False
    
    with open(file_path, "r") as f:
        existing_ids = f.read().splitlines()
        return target_id in existing_ids

def save_id(target_id: str, filename: str, name: str):
    """Helper method: Saves the unique ID to the target ID file in the directory."""
    if not os.path.exists("ids"):
        os.makedirs("ids")
        
    file_path = os.path.join("ids", filename)

    with open(file_path, "a") as f:
        f.write(f"{name}: {target_id}\n")

class User:
    def __init__(self, user_name: str, is_admin: bool):
        self.user_name = user_name
        self.is_admin = is_admin
        self.user_id = self.generate_user_id()

    def generate_user_id(self) -> str:
        while True:
            prefix = "ADM" if self.is_admin else "USR"
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            new_id = f"{prefix}-{random_part}"

            if not check_id_exists(new_id, "userids"):
                save_id(new_id, "userids", self.user_name)
                return new_id

    def __str__(self):
        return self.user_name


class Player(User):
    def __init__(self, player_name: str, position: str, is_admin = False):
        super().__init__(player_name, is_admin)
        self.position = position
        self._teams: list[Team] = []
        self.user_id = self.generate_player_id()

    def generate_player_id(self) -> str:
        while True:
            prefix = "ADM" if self.is_admin else "PLR"
            random_part = "".join(random.choices(string.digits, k=6))
            new_id = f"{prefix}-{random_part}"
            
            if not check_id_exists(new_id, "playerids"):
                save_id(new_id, "playerids", self.user_name)
                return new_id
    

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
        super().__init__(match_official_name, is_admin=False)
        self.user_id = self.generate_official_id()

    def generate_official_id(self) -> str:
        while True:
            prefix = "OFF"
            random_part = ''.join(random.choices(string.digits, k=6))
            new_id = f"{prefix}-{random_part}"

            if not check_id_exists(new_id, "officialids"):
                save_id(new_id, "officialids",self.user_name)
                return new_id

    def __str__(self):
        return f"Match official name:{self.user_name}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, MatchOfficial):
            return False
        return self.user_name == other.user_name


class Team:
    def __init__(self, team_name: str, captain: Player):
        self.team_name = team_name
        self.team_id = self.generate_team_id()
        self.roster: list[Player] = []
        self.captain: Player = captain


    def generate_team_id(self) -> str:
        while True:
            initials = "".join([word[0].upper() for word in self.team_name.split()])[:3]
            random_part = ''.join(random.choices(string.digits, k=4))
            new_id = f"TM-{initials}-{random_part}"
            if not check_id_exists(new_id, "teamids"):
                save_id(new_id, "teamids", self.team_name)
                return new_id

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

    def is_captain(self, player: User | Player) -> bool:
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
            #This line ensures that both condition return not(False)= True before executing the next block
            raise PermissionError(f"You do not have permission to add players")

        if not self.check_in_team(player):
            self.roster.append(player)
            return f"Player was Successfully added"
        else:
            raise ValueError(f"{player} is already in the team!")

    def remove_player(self, actor: User | Player, player: Player) -> None:
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
    def __init__(self, league_name: str, league_size: int, sport: str, creator: User):
        self.creator = creator
        self.league_name = league_name
        self.league_id = self.generate_league_id()
        self.league_size = league_size
        self._status = LeagueStatus.REGISTERING
        self.matches: list[League.Match] = []
        self.registered_match_officials: list[MatchOfficial] = [MatchOfficial("Jerry Cooper")]
        self.teams: list[Team] = []
        self.sport = sport.capitalize()
        self.population_check(self.creator)

    def generate_league_id(self) -> str:
        while True:
            initials = "".join([word[0].upper() for word in self.league_name.split()])[:3]
            year = time.strftime("%Y")
            random_part = ''.join(random.choices(string.ascii_uppercase, k=3))
            new_id = f"LG-{initials}-{year}-{random_part}"
            if not check_id_exists(new_id, "leagueids"):
                save_id(new_id, "leagueids", self.league_name)
                return new_id

    def populate_league(self, actor: User, deficit: int):
        """Guarded method: Only Administrators can manage League states"""

        if not check_admin(actor):
            raise PermissionError(f"Only Administrators can manage league states")
        if self.check_league_status() != LeagueStatus.REGISTERING:
            raise ValueError(f"League is not in the REGISTERING state!")

        if deficit < 0:
            raise ValueError(f"League size cannot be negative!")

        for i in range(deficit):
            team_name = Prompt.ask(f"Enter the name of the team #{i + 1}")
            captain_name = Prompt.ask(f"Enter the name of the captain of team #{i + 1}")
            captain_position = Prompt.ask(f"Enter the position of the captain of team #{i + 1}")

            team = Team(team_name, Player(captain_name, captain_position))
            self.teams.append(team)
            self.update_league_status(actor, new_status="REGISTERED")

    def population_check(self, actor: User) -> int:
        """Helper method to encapsulate population check"""
        if len(self.teams) < self.league_size:
            if len(self.teams) == 0:
                self.populate_league(actor, self.league_size)
                return self.league_size

            else:
                self.populate_league(actor, (self.league_size - len(self.teams)))
                return self.league_size

        elif len(self.teams) > self.league_size:
            self.teams= []
            self.populate_league(actor, self.league_size)

            raise ValueError(f"League size cannot exceed {self.league_size}!")

        elif len(self.teams) == self.league_size:
            return True

        return False

    def fetchOfficials(self):
        return self.registered_match_officials

    def update_league_status(self, actor: User, new_status: str):
        """Guarded method: To prevent regular users from changing League States"""
        if not check_admin(actor):
            raise PermissionError(f"Only Administrators can modify League State!")

        for state in LeagueStatus:
            if state.value == new_status:
                self._status = new_status
                return "Done"
        return f"Chosen state not Valid"

    def is_registered_official(self, official: MatchOfficial) -> bool:
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
            while True:
                unique_match_index: int = len(self.container_league.matches) + 1
                home_acr = self.home_team.team_name[:2].upper()
                away_acr = self.away_team.team_name[:2].upper()
                league_acr = "".join([word[0].upper() for word in self.container_league.league_name.split()])[:3]

                new_id = f"MCH-{league_acr}-{home_acr}{away_acr}-{unique_match_index:03d}"
                if not check_id_exists(new_id, "matchids"):
                    save_id(new_id, "matchids", "")
                    return new_id

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
                new_time = Prompt.ask(f"Enter a new match date and time in the order DD-MM-YYYY HH:MM")
                self.match_datetime = new_time


    class RuleSet:
        ruleSet: dict = {
            "WIN": "",
            "DRAW": "",
            "LOSS": "",
            "OFFENCE": ""
        }

        temp_ruleSet = deepcopy(ruleSet)

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

    def check_league_status(self):
        return self._status


def check_admin(actor: User) -> bool:
    """Helper method: To encapsulate Admin check"""
    return actor.is_admin == True

