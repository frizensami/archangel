# FROMS
from models import Player
from graph import get_graph_from_edges, draw_graph, get_full_cycles_from_graph,\
    full_cycle_to_edges, get_one_full_cycle, convert_full_cycle_to_graph,\
    get_one_full_cycle_from_graph, get_hamiltonian_path_from_graph,\
    is_there_definitely_no_hamiltonian_cycle, hamilton
import networkx as nx
import time
import random
from random import shuffle
from random import randint

# Constants
GENDER_MALE = "Male"
GENDER_FEMALE = "Female"
GENDER_NONBINARY = "Non-binary"
GENDER_NOPREF = "No preference"


DISPLAY_GRAPH = True

# Changing this value changes how much we care about the houses of players being the same
# If 1 - we don't care, and house de-conflicting is ignored. 0 means we won't allow any players of the same house to be matched.
RELAX_SAME_HOUSE_REQUIREMENT_PERCENTAGE = 0.00

RELAX_SAME_FACULTY_REQUIREMENT_PERCENTAGE = 0.00


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
        raise ValueError('Floor provided (' + player.floor +
                         ') for player ' + str(player) + ' is invalid!')


def is_gender_pref_respected(player_being_checked, other_player):
    if player_being_checked.gender_pref == GENDER_NOPREF:
        # If they have no preference, always respected
        print "Nopref"
        return True
    else:
        # Otherwise check if the other_player gender is what is wanted
        gender_pref_respected = player_being_checked.gender_pref == other_player.gender
        return gender_pref_respected


def are_gender_prefs_respected(angel_player, mortal_player):
    return is_gender_pref_respected(angel_player, mortal_player) and \
        is_gender_pref_respected(mortal_player, angel_player)


def is_there_edge_between_players(angel_player, mortal_player):
    '''
    Checks if two players are valid as an angel-mortal pair i.e. an "edge"
    exists between them. If we are enforcing a heterogenous gender mix for these
    players - check if they are of the same gender and return False (no edge)
    between them
    '''
    print "Checking %s and %s" % (angel_player, mortal_player)

    # Check if gender choice is respected
    gender_pref_is_respected = are_gender_prefs_respected(
        angel_player, mortal_player)

    # Check house and faculty are not the same
    random_relax_fac_requirement = random.random() < RELAX_SAME_FACULTY_REQUIREMENT_PERCENTAGE
    if random_relax_fac_requirement:
        players_are_from_same_faculty = False
    else:
        players_are_from_same_faculty = angel_player.faculty == mortal_player.faculty

    # Relax house requirement
    random_relax_house_requirement = random.random() < RELAX_SAME_HOUSE_REQUIREMENT_PERCENTAGE
    if random_relax_house_requirement:
        players_are_from_same_house = False
    else:
        players_are_from_same_house = get_house_from_player(
            angel_player) == get_house_from_player(mortal_player)

    valid_pairing = not (players_are_from_same_faculty) and  gender_pref_is_respected and (not  players_are_from_same_house)# Remove same-house reqr -->  #or players_are_from_same_house) and
    if players_are_from_same_faculty:
        print "players from same fac\n"
    #ignore this requirement
    if players_are_from_same_house:
        print "players from same house\n"
    if not gender_pref_is_respected:
        print "gender pref not respected"

    print "\n"

    return valid_pairing


def get_player_edges_from_player_list(player_list):
    player_edges = []
    # iterate through all players in list - compare each player to all others
    for player in player_list:
        for other_player in player_list:
            if other_player != player:
                if is_there_edge_between_players(player, other_player):
                    player_edges.append((player, other_player))

    return player_edges


def angel_mortal_arrange(player_list):
    '''
    Depending on the gender preferences to follow, run the edge-finding
    algorithm, generate a graph and find a Hamiltonian circuit.
    '''
    print "Arranging player list: %s" % player_list
    # Convert the list of players into a list of valid edges
    player_edges = get_player_edges_from_player_list(player_list)
    # Generate the overall graph from all edges
    overall_graph = get_graph_from_edges(player_edges)
    print "Number of nodes in overall graph: " + str(overall_graph.number_of_nodes())
    # Find all connected components and find cycles for all
    graphs = list(overall_graph.subgraph(c) for c in
                  nx.strongly_connected_components(overall_graph)) ##.strongly_connected_component_subgraphs(overall_graph) is deprecated in version 2.4 https://stackoverflow.com/questions/61154740/attributeerror-module-networkx-has-no-attribute-connected-component-subgraph

    print "\nConnected components detected: %s" % len(graphs)

    print "Printing original player list: "
    for player in player_list:
        print player

    print "\n\n"

    
    print "Player list size: " + str(len(player_list))

    list_of_player_chains = []

    #for G in graphs:
     #   draw_graph(G)

    for G in graphs:

        print "Printing players in current graph:"
        for graph_player in G.nodes():
            print graph_player
        
        # Draw this intermediate graph
        print "Number of nodes in graph: " + str(G.number_of_nodes())
        if DISPLAY_GRAPH:
            draw_graph(G)

        # Find out if there is DEFINITELY no hamiltonian cycle
        is_there_full_cycle = is_there_definitely_no_hamiltonian_cycle(G)
        print "Is there DEFINITELY no full cycle? - %s" % is_there_full_cycle
        # Sleep for a few seconds
        time.sleep(2)
        '''
        # Output all cycles that encompass all nodes (valid pairings)
        full_cycles = get_full_cycles_from_graph(G)
        # Pick any full cycle to draw, or draw nothing if there are no full cycles
        full_cycle = get_one_full_cycle(full_cycles)
        '''
        full_cycle = hamilton(G) #get_one_full_cycle_from_graph(G)
        #full_cycle = get_hamiltonian_path_from_graph(G)
        # Draw the full cycle if it exists
        if full_cycle is not None:
            G_with_full_cycle = convert_full_cycle_to_graph(full_cycle)
            draw_graph(G_with_full_cycle)
            list_of_player_chains.append(full_cycle)
        else:
            print "There is no full cycle - sorry! This means that the current set of players cannot form a perfect chain given the arrange requirements"

    return list_of_player_chains
