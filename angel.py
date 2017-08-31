'''
tAngel angel-mortal matching code
Author: Sriram Sami
Version: 0.0.1



Program input: List of participants
Program output: Participants matched to each other forming either a) one complete ring or b) multiple complete rings. No lone particpants are allowed.

Priorities (decreasing order) [must be done]:
1) Forming complete circles (everyone MUST have an angel and mortal)
2) Respecting gender choices

Optimization objective - get people you DON'T KNOW AT ALL
Optimization priorities:
1) Angel - Mortal relationship - they must not know each other as much as possible
- Achieved by separating by HOUSE (floor) and FACULTY

Distance (or whether an edge exists between two nodes) is a function of:
1) Whether they are of different houses
2) Whether their faculties are different
'''
# IMPORTS
import csv
import time
import random

# FROMS
from models import Player
from arrange import angel_mortal_arrange

# GLOBALS
PLAYERFILE = "playerlist.tsv"

# Constants
GENDER_MALE = "Male"
GENDER_FEMALE = "Female"
GENDER_NONBINARY = "Non-binary"
GENDER_NOPREF = "No preference"

GENDER_SWAP_PREFERENCE_PERCENTAGE = 0.2

def read_csv(filename):
    '''
    Reads a CSV file and outputs a list of Player objects
    '''
    person_list = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            new_person = Player(name=row[1].decode('ascii', errors='ignore'),
                                fbname=row[2],
                                floor=row[3],
                                room_number=row[4],
                                contact_number=row[5],
                                gender=row[6],
                                year=row[7],
                                gender_pref=row[8],
                                faculty=row[9],
                                interests=row[10])
            if new_person.is_valid():
                person_list.append(new_person)
                print "Adding " + str(new_person)
            else:
                print "Invalid person during csv reading: " + str(row)
    return person_list

'''
@unused
'''
def separate_players(player_list):
    '''
    Separates the list of player list into male_male, male_female, and
    female_female gender preference lists
    '''
    male_male_list = []
    male_female_list = []
    female_female_list = []

    for player in player_list:
        print "Player: %s, Gender: %s, GenderPref: %s" % (player, player.gender, player.gender_pref)
        if (player.gender == 'Male' and player.gender_pref == 'Male') or (player.gender == "Non-binary" and player.gender_pref == "Male"):
            male_male_list.append(player)
        elif (player.gender == 'Female' and player.gender_pref == 'Female') or (player.gender == "Non-binary" and player.gender_pref == "Female"):
            female_female_list.append(player)
        else:
            male_female_list.append(player)

    return (male_male_list, male_female_list, female_female_list)


def write_to_csv(index, *player_lists):
    '''
    Writes a variable number of player lists to csv
    '''
    for player_list in player_lists:
        if player_list is not None:
            print "Length of list: %s" % len(player_list)

            cur_time = time.strftime("%Y-%m-%d %H-%M-%S")
            f = open(str(index) + '-' + cur_time + ".csv", "w")
            for player in player_list:
                f.write(player.to_csv_row())
                f.write("\n")
            # write the first player again to close the loop
            f.write(player_list[0].to_csv_row())
            f.write("\n")
            f.close()


def modify_player_list(player_list):
        # Force hetero mix
        for player in player_list:
                if player.gender_pref == GENDER_NOPREF:
                        random_change_preference = random.random() < GENDER_SWAP_PREFERENCE_PERCENTAGE
                        if player.gender == GENDER_MALE and random_change_preference:
                                print "Male -> Female"
                                player.gender_pref = GENDER_FEMALE
                        elif player.gender == GENDER_FEMALE and random_change_preference:
                                print "Female -> Male"
                                player.gender_pref = GENDER_MALE

if __name__ == "__main__":
    print "\n\n"
    print "============================================="
    print "tAngel 2016 engine initializing.............."
    print "============================================="
    print "\n\n"

    # Get list of Player objects from csv file
    player_list = read_csv(PLAYERFILE)
    # Map the player list through any neccessary transformations
    modify_player_list(player_list)
    # separate the players into player-chains (connected components)
    list_of_player_chains = angel_mortal_arrange(player_list)
    # Write each chain to a separate csv
    for index, player_chain in enumerate(list_of_player_chains):
        write_to_csv(index, player_chain)
