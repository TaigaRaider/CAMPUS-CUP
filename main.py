from classes import *


def main():
    team1 = Team("Juggernaut FC")
    team1.add_player("Jay", "RW")
    team1.add_player("Jordan", "LW")
    team1.add_player("Shamika", "LW")
    team1.add_player("Tadina", "CF")
    team1.add_player("Divine", "CDM")
    team1.add_player("David", "LM")
    team1.add_player("Taiwo", "LCB")
    team1.add_player("Mikel", "RCB")
    team1.add_player("Jason", "RB")
    team1.add_player("Michael", "RM")
    team1.add_player("Johnson", "LAM")
    team1.add_player("Yvonik", "CAM")
    team1.add_player("Allen", "SS")
    team1.add_player("Lamar", "GK")

    print(team1.appoint_captain("Jay", "RW"))

    team1.remove_player("Mikel", "RCB")
    team1.remove_player("Jason", "RB")
    team1.remove_player("taiwo", "LCB")

    print(team1.check_in_team("Jay", "RW"))
    print(team1.check_in_team("Mikel", "RCB"))
    print(team1.check_in_team("Jason", "RB"))
    print(team1.check_in_team("Taiwo", "LCB"))

    print(team1.fetch_squad())


if __name__ == '__main__':
    main()
