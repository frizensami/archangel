# FROMS
from models import Player
from graph import get_graph_from_edges, draw_graph, get_full_cycles_from_graph, full_cycle_to_edges, draw_one_full_cycle
import networkx as nx
from random import shuffle

def get_house_from_player(player):
    if player.floor == 3:
        return "prof"
    elif player.floor >= 4 and player.floor <= 7:
        return "shan"
    elif player.floor >= 8 and player.floor <= 11:
        return "ora"
    elif player.floor >= 12 and player.floor <= 14:
        return "gaja"
    elif player.floor >= 15 and player.floor <= 18:
        return "tancho"
    elif player.floor >= 19 and player.floor <= 21:
        return "ponya"
    else:
        raise ValueError('Floor provided (' + player.floor + ') for player ' + str(player) + ' is invalid!')


def is_there_edge_between_players(angel_player, mortal_player, single_gender=False):
    '''
    Checks if two players are valid as an angel-mortal pair i.e. an "edge"
    exists between them. If we are enforcing a heterogenous gender mix for these
    players - check if they are of the same gender and return False (no edge)
    between them
    '''
    print "Checking %s and %s" % (angel_player, mortal_player)

    players_are_same_gender = angel_player.gender == mortal_player.gender
    if (not single_gender) and players_are_same_gender:
        return True # MUST BE FALSE
    else:
        # Check house and faculty are not the same
        players_are_from_same_faculty = angel_player.faculty == mortal_player.faculty
        players_are_from_same_house = get_house_from_player(angel_player) == get_house_from_player(mortal_player)
        valid_pairing = not (players_are_from_same_faculty or players_are_from_same_house)

        return valid_pairing


def get_player_edges_from_player_list(player_list, single_gender):
    player_edges = []
    # iterate through all players in list - compare each player to all others
    for player in player_list:
        for other_player in player_list:
            if other_player != player:
                if is_there_edge_between_players(player, other_player, single_gender=single_gender):
                    player_edges.append((player, other_player))

    return player_edges


def angel_mortal_arrange(player_list, single_gender=False):
    '''
    All players in list are interchangeable - same gender, so we can
    just naively compute distance between all of them
    '''
    print "Arranging player list: %s" % player_list
    # Convert the list of players into a list of valid edges
    player_edges = get_player_edges_from_player_list(player_list, single_gender)
    # Generate the overall graph from all edges
    G = get_graph_from_edges(player_edges)
    # Output all cycles that encompass all nodes (valid pairings)
    full_cycles = get_full_cycles_from_graph(G)
    # Pick any full cycle to draw, or draw nothing if there are no full cycles
    draw_one_full_cycle(full_cycles)
