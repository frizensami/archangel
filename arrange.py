# FROMS
from models import Player
from graph import get_graph_from_edges, draw_graph, get_full_cycles_from_graph, \
    full_cycle_to_edges, get_one_full_cycle, convert_full_cycle_to_graph, \
    get_one_full_cycle_from_graph, get_hamiltonian_path_from_graph, \
    is_there_definitely_no_hamiltonian_cycle, hamilton

import datetime
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=f'logs/{datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")}.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

import networkx as nx
import time
import random
# from random import shuffle
from random import randint

# Constants
GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_NONBINARY = "non-binary"
GENDER_NOPREF = "no preference"

DISPLAY_GRAPH = True

MINIMUM_MATCHED_PLAYERS_BEFORE_CSVOUTPUT = 0.8  ##Proportion minimum of total player count in accepted csv before 2 csvs will be outputted (1st accepted players list, 2nd rejected players list

RELAX_GENDERPREF_REQUIREMENT_PERCENTAGE = 0.35

RELAX_NO_SAME_HOUSE_REQUIREMENT_PERCENTAGE = 0.35
# Changing this value changes how much we care about the houses of players being the same
# If 1 - we don't care, and house de-conflicting is ignored. 0 means we won't allow any players of the same house to be matched.

RELAX_NO_SAME_CG_REQUIREMENT_PERCENTAGE = 0.00


# RELAX_NO_SAME_FACULTY_REQUIREMENT_PERCENTAGE = 0.00 #not used


def get_house_from_player(player):
    if player.housenumber == "":
        raise ValueError('House number provided ' + player.housenumber +
                         ' for player ' + str(player.username) + ' is invalid!')


def get_cg_from_player(player):
    if (player.cgnumber == ""):
        return str(randint(60, 8888))  # Nursing has no CGs, thus we do not want to conflict with Medicine CGs 1-60
    else:
        return player.cgnumber


def is_gender_pref_respected(player_being_checked, other_player):
    if player_being_checked.genderpref == GENDER_NOPREF:
        # If they have no preference, always respected
        # print (f"No gender pref")
        return True
    else:
        # Otherwise check if the other_player gender is what is wanted
        gender_pref_respected = player_being_checked.genderpref == other_player.genderplayer
        return gender_pref_respected


def are_gender_prefs_respected(angel_player, mortal_player):
    return is_gender_pref_respected(angel_player, mortal_player) and \
           is_gender_pref_respected(mortal_player, angel_player)


def is_there_edge_between_players(angel_player, mortal_player):
    '''
    Checks if two players are valid as an angel-mortal pair i.e. an "edge"
    exists between them. E.g. If we are enforcing a heterogenous gender mix for these
    players - check their gender preferences and return False (no edge)
    between them
    '''
    print(f"Checking {angel_player} and {mortal_player}")

    # Check if gender choice is respected
    random_relax_genderpref_requirement = random.random() < RELAX_GENDERPREF_REQUIREMENT_PERCENTAGE
    if random_relax_genderpref_requirement:
        gender_pref_is_respected = True
    else:
        gender_pref_is_respected = are_gender_prefs_respected(
            angel_player, mortal_player)

    # # Check house and faculty are not the same

    '''
    no same faculty requirement is not used
    '''
    # random_relax_fac_requirement = random.random() < RELAX_SAME_FACULTY_REQUIREMENT_PERCENTAGE
    # if random_relax_fac_requirement:
    #     players_are_from_same_faculty = False
    # else:
    #     players_are_from_same_faculty = angel_player.faculty == mortal_player.faculty

    # Relax no same house requirement
    random_relax_house_requirement = random.random() < RELAX_NO_SAME_HOUSE_REQUIREMENT_PERCENTAGE
    if random_relax_house_requirement:
        players_are_from_same_house = False
    else:
        players_are_from_same_house = get_house_from_player(
            angel_player) == get_house_from_player(mortal_player)

    # Relax no same CG requirement
    random_relax_cg_requirement = random.random() < RELAX_NO_SAME_CG_REQUIREMENT_PERCENTAGE
    if random_relax_cg_requirement:
        players_are_from_same_cg = False
    else:
        players_are_from_same_cg = get_cg_from_player(
            angel_player) == get_cg_from_player(mortal_player)

    valid_pairing = gender_pref_is_respected and (not players_are_from_same_house) and (
        not players_are_from_same_cg)  # and (not players_are_from_same_faculty) # Remove same-house reqr -->  #or players_are_from_same_house) and
    # if players_are_from_same_faculty:
    #     print (f"players from same fac\n")
    # ignore this requirement
    if not gender_pref_is_respected:
        print(f"gender pref not respected")
    if players_are_from_same_house:
        print(f"players from same house\n")
    if players_are_from_same_cg:
        print(f"players from same CG\n")

    print(f"\n")

    return valid_pairing


def get_player_edges_from_player_list(player_list):
    player_edges = []
    # iterate through all players in list - compare each player to all others
    for player in player_list:
        for other_player in player_list:
            if other_player != player:
                if is_there_edge_between_players(player, other_player):
                    player_edges.append((player, other_player))
                else:
                    logger.info(f"{player} and {other_player} have conflicts")  # to keep track who was rejected
    return player_edges


def angel_mortal_arrange(player_list):
    '''
    Depending on the gender preferences to follow, run the edge-finding
    algorithm, generate a graph and find a Hamiltonian circuit.
    '''
    print(f"Arranging player list: {player_list}")
    # Convert the list of players into a list of valid edges
    player_edges = get_player_edges_from_player_list(player_list)
    # Generate the overall graph from all edges
    overall_graph = get_graph_from_edges(player_edges)
    print(f"Number of nodes in overall graph: {overall_graph.number_of_nodes()}")
    # Find all connected components and find cycles for all
    graphs = list(overall_graph.subgraph(c) for c in
                  nx.strongly_connected_components(
                      overall_graph))  ##.strongly_connected_component_subgraphs(overall_graph) is deprecated in version 2.4 https://stackoverflow.com/questions/61154740/attributeerror-module-networkx-has-no-attribute-connected-component-subgraph

    print(f"\nConnected components detected: {len(graphs)}")

    print(f"Printing original player list: ")
    for player in player_list:
        print(f"{player}")
    print(f"Original player list size: {len(player_list)}")
    print(f"\n\n")

    list_of_player_chains = []

    # for G in graphs:
    #    draw_graph(G)

    for G in graphs:

        print(f"Printing players in current graph:")
        for graph_player in G.nodes():
            print(f"{graph_player}")

        # Draw this intermediate graph
        print(f"Number of nodes in graph: {G.number_of_nodes()}")
        if DISPLAY_GRAPH:
            draw_graph(G)
        # Find out if there is DEFINITELY no hamiltonian cycle
        is_there_full_cycle = is_there_definitely_no_hamiltonian_cycle(G)
        print(f"Is there DEFINITELY no full cycle? - {is_there_full_cycle}")
        # Sleep for a few seconds
        time.sleep(2)
        '''
        # Output all cycles that encompass all nodes (valid pairings)
        full_cycles = get_full_cycles_from_graph(G)
        # Pick any full cycle to draw, or draw nothing if there are no full cycles
        full_cycle = get_one_full_cycle(full_cycles)
        '''
        full_cycle = hamilton(G)  # get_one_full_cycle_from_graph(G)
        # full_cycle = get_hamiltonian_path_from_graph(G)
        # Draw the full cycle if it exists
        if full_cycle is not None and (G.number_of_nodes() >= (MINIMUM_MATCHED_PLAYERS_BEFORE_CSVOUTPUT * len(
                player_list))):  # do not print CSV if number of nodes is < 80% of participants
            G_with_full_cycle = convert_full_cycle_to_graph(full_cycle)
            draw_graph(G_with_full_cycle)
            list_of_player_chains.append(full_cycle)
            # find out which nodes were missing
            players_not_in_csv = set(player_list) - set(list(G.nodes()))
            logger.info(
                f"CSV has been printed. However, the following players {players_not_in_csv} are not inside. Please match them manually.")
            print(
                f"Found a full cycle! CSV is printed. However, the following players {players_not_in_csv} are not inside. Please match them manually.")
        else:
            print(
                f"There is no full cycle - sorry! This means that the current set of players cannot form a perfect chain given the arrange requirements. No CSV printed.")
            logger.info(f"CSV not printed - no full cycle found")

    return list_of_player_chains
