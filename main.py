from classes import *


def main():
    team1 = Team("Juggernaut FC")
    player1 = Player("Jay", "RW")
    player2 = Player("Jordan", "LW")

    team1.add_player(player1)
    team1.add_player(player2)

    # print(team1.appoint_captain("Jay", "RW"))

    team1.remove_player(player1)

    print(team1.check_in_team(player1))
    print(team1.check_in_team(player2))

    print(team1.players)


if __name__ == '__main__':
    main()
