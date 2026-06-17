from classes import *


def main():


    player1 = Player("Jay", "RW")
    player2 = Player("Jordan", "LW")
    player3 = Player("Jack", "CF")

    team1 = Team("Juggernaut FC")
    team2 = Team("Liverpool FC")

    team1.add_player(player1)
    team1.add_player(player2)
    team1.add_player(player3)
    print(team1.appoint_team_captain(player1))

    team1.remove_player(player1)

    league= League("Premier League", 3)
    match1 = league.Match(team1, team2, league.league_name)
    print(league.status)


if __name__ == '__main__':
    main()
