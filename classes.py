import time
from abc import ABC, abstractmethod
from typing import Any

from rich.progress import track
from rich.prompt import Prompt


class User(ABC):
    @abstractmethod
    def __init__(self, user_name: str):
        self.user_name = user_name

    @abstractmethod
    def __str__(self):
        return self.user_name


class Player(User):
    def __init__(self, player_name: str, position: str):
        self.player_name = player_name
        self.position = position

    def __str__(self):
        return f"{self.player_name}"

    def __repr__(self):
        return f"Player name:{self.player_name}\n Position: {self.position}\n"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return self.player_name == other.player_name and self.position == other.position


class Admin(User):
    def __init__(self, admin_name: str):
        self.admin_name = admin_name

    def __str__(self):
        return f"Admin name:{self.admin_name}"


class MatchOfficial(User):
    def __init__(self, match_name: str):
        self.match_official_name = match_name

    def __str__(self):
        return f"Match official name:{self.match_official_name}"


class Team:
    def __init__(self, team_name: str):
        self.team_name = team_name
        self.players: list[Player] = []

    def __str__(self):
        return f"Team name: {self.team_name}"

    def __repr__(self):
        return f"Team name: {self.team_name}\n Players: {self.players}"

    def __hash__(self) -> int:
        return hash(self.team_name)

    def __len__(self) -> int:
        return len(self.players)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Team):
            return False
        return self.team_name == other.team_name

    def check_in_team(self, player_name: str, position: str) -> bool:
        player: Player | Team.TeamCaptain
        for player in self.players:
            if player.player_name == player_name and player.position == position:
                return True
            else:
                return False

        return False

    def find_in_team(self, player_name: str, position: str) -> int | None:
        for player in self.players:
            if player.player_name == player_name and player.position == position:
                return self.players.index(player)
            else:
                if type(player) == self.TeamCaptain:
                    return self.players.index(player)
        return None

    def add_player(self, player_name: str, position: str):
        if not self.check_in_team(player_name, position):
            new_player = Player(player_name, position)
            self.players.append(new_player)
            print(f"{new_player} was Successfully Added!")
        else:
            raise ValueError(f"{player_name} is already in the team!")

    def remove_player(self, player_name: str, position: str) -> None:
        for player in self.players:
            if player.player_name == player_name and player.position == position:
                self.players.remove(player)

    def sys_fetch_squad(self):
        return list(self.players)

    def fetch_squad(self) -> Any | None:
        for player in self.players:
            formatted_player = (f"{self.players.index(player) + 1}. |\tName: {player.player_name}\t|\n"
                                f"   |\tPosition: {player.position}\t|")
            print(formatted_player)
        print(f"\nSquad Fetch Complete!")

    def appoint_captain(self, player_name: str, position: str):
        message: str = ""
        for player in self.players:
            if player.player_name == player_name and player.position == position:
                self.remove_player(player_name, position)
                team_captain = self.TeamCaptain(player_name, position)
                self.players.append(team_captain)

                message = f"{player} was Successfully Appointed as Team Captain!"

        return message

    class TeamCaptain(Player):
        def __init__(self, team_captain_name: str, position: str):
            super().__init__(team_captain_name, position)

        def __eq__(self, other):
            if not isinstance(other, Player):
                return False
            else:
                return self.player_name == other.player_name and self.position == other.position

        def __repr__(self):
            return f"Team Captain name: {self.player_name}\n Position: {self.position}\n"

    class Formation:
        def __init__(self, formation_name: str, use_case: str):
            self.formation_name = formation_name
            self.use_case = use_case

    class PracticeSession:
        def __init__(self, session_name: str, session_date: str, session_time: str):
            self.session_name = session_name
            self.session_date = session_date
            self.session_time = session_time


def generate_match_id():
    


class League:
    def __init__(self, league_name: str):
        self.league = league_name

    class Match:
        match_ids: list[int] = []

        def __init__(self, home_team: Team, away_team: Team):
            self.match_id = generate_match_id()
            self.home_team = home_team
            self.away_team = away_team
            self.match_status = ""
            self.match_location = ""
            self.home_team_score = 0
            self.away_team_score = 0
            self.match_officials :list[MatchOfficial] = []
            self.start_time= ""
            self.end_time = ""


        def __str__(self):
            return f"{self.home_team} vs {self.away_team}"

        def __repr__(self):
            return f"Team 1:{self.home_team}\nTeam 2:{self.away_team}\nStatus:{self.match_status}"

        def start_match(self):
            pass

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

        def reschedule_match(self):
            pass


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
                    print(f"{self.ruleSet}\n Update Successfully Reverted!")

                case _:
                    print(f"Invalid Input")
