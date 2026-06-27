from classes import *


def main():
    user_admin1 = User(user_name="Admin", is_admin=True)

    official1 = MatchOfficial("Jerry Cooper")

    player1 = Player("Jay", "RW")
    player2 = Player("Jordan", "LW")
    player3 = Player("Jack", "CF")
    player4 = Player("TestCap", "RB")
    player5 = Player("TestCap2", "RB")

    team1 = Team("Juggernaut FC", player4)
    team2 = Team("Liverpool FC", player5)

    team1.add_player(user_admin1, player4)
    team1.add_player(user_admin1, player1)

    print(team1.appoint_team_captain(user_admin1, player4))

    team1.add_player(player4, player2)
    team1.add_player(player4, player3)

    team1.remove_player(player4, player1)

    league = League("Premier League", 5, "football", user_admin1)
    league.teams.append(team1)
    print(league.is_registered_official(official1))

    match1 = league.Match(team1, team2, league)
    print(league.update_league_status(actor=user_admin1, new_status="REGISTERED"))
    print(league.status)

    print(team1)
if __name__ == '__main__':
    main()
