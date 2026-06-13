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

    league= League("Premier League")
    match1 = league.Match(team1, team2, league.league)
    print(match1.match_id)






    # print(team1.check_in_team(player1))
    # print(team1.check_in_team(player2))
    # print(team1.check_in_team(player3))
    #
    # print(team1.players)


if __name__ == '__main__':
    main()
