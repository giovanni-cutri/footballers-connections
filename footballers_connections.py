import argparse
import bs4
import lxml
import requests
import sys
import urllib.parse
import validators

from util import Node, StackFrontier, QueueFrontier

base_url = "https://www.worldfootball.net"

def main():

    if len(sys.argv) == 3:
        (initial_player, final_player) = parse_arguments()

    elif len(sys.argv) == 1:
        initial_player = input("Worldfootball URL of the initial player: ")
        final_player = input("Worldfootball URL of the final player: ")

    else:
        sys.exit("Invalid usage.")

    source = validate_player(initial_player)
    if source is None:
        sys.exit("Initial player not found.")
    target = validate_player(final_player)
    if target is None:
        sys.exit("Final player not found.")

    path = shortest_path(source, target)
    
    print_result(path, source)


def shortest_path(source, target):
    """
    Returns the shortest list of teams
    that connect the source to the target.

    If no possible path, returns None.
    """

    # If source and target coincide, return empty path
    if source == target:
        return ""

    # Keep track of number of states explored
    num_explored = 0

    # Initialize frontier to just the starting position
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    # Initialize an empty explored set
    explored = set()

    # Keep looping until solution found
    while True:

        # If nothing left in frontier, then no path
        if frontier.empty():
            return None

        # Choose a node from the frontier
        node = frontier.remove()
        num_explored += 1

        # Mark node as explored
        explored.add(node.state)

        # Add neighbors to frontier
        for action,state in neighbors_for_player(node.state):

            if not frontier.contains_state(state) and state not in explored:

                child = Node(state=state, parent=node, action=action)
  
                # If node is the goal, then we have a solution
                if child.state == target:
                    teams = []
                    players = []
                    while child.parent is not None:
                        teams.append(child.action)
                        players.append(child.state)
                        child = child.parent
                    teams.reverse()
                    players.reverse()
                    solution = list(zip(teams, players))
                    return solution
                
                frontier.add(child)


def parse_arguments():
    """
    Parses command-line arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("initial_player", help="the Worldfootball URL of the player from whom you want to start the search")
    parser.add_argument("final_player", help="the Worldfootball URL of the player who must be reached")
    args = parser.parse_args()
    return (args.initial_player, args.final_player)


def validate_player(player):
    """
    Validates the player provided by the user
    """

    if not validators.url(player) or "worldfootball.net/player_summary/" not in player:
        return None
    
    res = requests.get(player)
    if res.status_code == 200:
        return player
    
    return None


def neighbors_for_player(player):
    """
    Returns (team_id, player_id) pairs for players
    who played for the same team of the given player
    """
    res = requests.get(player)
    soup = bs4.BeautifulSoup(res.text, "lxml")

    teams_ids = {base_url + page.attrs["href"] for page in soup.select("div table a[href^='/teams/']")}  # set comprehension

    neighbors = set()
    
    for team_id in teams_ids:
        res = requests.get(team_id + "10/")
        soup = bs4.BeautifulSoup(res.text, "lxml")
        players_ids = [base_url + player.attrs["href"] for player in soup.select("a[href^='/player']")]

        for player_id in players_ids:
            neighbors.add((team_id, player_id))

    return neighbors


def get_name(id):
    """
    Returns the corresponding name for the player / team provided as a parameter
    """

    res = requests.get(id)
    soup = bs4.BeautifulSoup(res.text, "lxml")
    return soup.select("title")[0].getText().strip()


def print_result(path, source):
    """
    Prints the resulting path
    """

    if path is None:
        print("\nPlayers are not connected.")
    elif path == "":
        print("\nIt's the same player.")
    else:
        degrees = len(path)
        if degrees == 1:
            print(f"\n{degrees} degree of separation.\n")
        else:
            print(f"\n{degrees} degrees of separation.\n")

        path = [(None, source)] + path

        for i in range(degrees):
            player1 = get_name(path[i][1])
            player2 = get_name(path[i + 1][1])
            team = get_name(path[i + 1][0])
            print(f"{i + 1}: {player1} and {player2} played for {team}")


if __name__ == "__main__":
    main()
