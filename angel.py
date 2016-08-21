'''
tAngel angel-mortal matching code
Author: Sriram Sami
Version: 0.0.1



Program input: List of participants + last year's tAngel list (no same angel/mortal)
Program output: Participants matched to each other forming either a) one complete ring or b) multiple complete rings. No lone particpants are allowed.

Priorities (decreasing order) [must be done]:
1) Forming complete circles (everyone MUST have an angel and mortal)
2) Respecting gender choices

Optimization objective - get people you DON'T KNOW AT ALL + similar interests
Optimization priorities:
1) Angel - Mortal relationship - they must not know each other as much as possible
- Achieved by separating by HOUSE (floor) and FACULTY


Algorithm:
1) Read in all CSV data, convert to custom objects
2) Split into 3 groups - M-M chain, M-F chain, F-F chain
3) For each chain:
        1) Calculate adjacency matrix (for all nodes in chain)
        2) Find euler tour
        3) That becomes the final chain

Distance (or whether an edge exists between two nodes) is a function of:
1) Whether they are of different houses
2) Whether their faculties are different
3) Whether they have been matched before


'''
# IMPORTS
import csv

# FROMS
from models import Player
from arrange import angel_mortal_arrange

# GLOBALS
PLAYERFILE = "playerlist.csv"


def read_csv(filename):
        '''
        Reads a CSV file and outputs a list of Player objects
        '''
        person_list = []
        with open(filename, 'rb') as f:
                reader = csv.reader(f, delimiter=",")
                for row in reader:
                        new_person = Player(name=row[1],
                                            fbname=row[2],
                                            floor=row[3],
                                            room_number=row[4],
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


def separate_players(player_list):
        '''
        Separates the list of player list into male_male, male_female, and
        female_female gender preference lists
        '''
        male_male_list = []
        male_female_list = []
        female_female_list = []

        for player in player_list:
                if player.gender == 'Male' and player.gender_pref == 'Male':
                        male_male_list.append(player)
                elif player.gender == 'Female' and player.gender_pref == 'Female':
                        female_female_list.append(player)
                else:
                        male_female_list.append(player)

        return (male_male_list, male_female_list, female_female_list)


def write_to_csv(*player_lists):
        '''
        Writes a variable number of player lists to csv
        '''
        for player_list in player_lists:
                print "\nWriting to csv not implemented :( \n"

                pass


if __name__ == "__main__":
        print "\n\n"
        print "============================================="
        print "tAngel 2016 engine initializing.............."
        print "============================================="
        print "\n\n"
        player_list = read_csv(PLAYERFILE)
        (male_male_list, male_female_list, female_female_list) = separate_players(player_list)

        print ""

        print "Male - Male list:"
        print str(male_male_list)
        print ""

        print "Male - Female list:"
        print str(male_female_list)
        print ""

        print "Male - Male list:"
        print str(female_female_list)
        print ""

        # Create the final chains from each filtered list
        male_male_chain = angel_mortal_arrange(male_male_list, single_gender=True)
        male_female_chain = angel_mortal_arrange(male_female_list, single_gender=False)
        female_female_chain = angel_mortal_arrange(female_female_list, single_gender=True)

        # Write the chains to CSV
        write_to_csv(male_male_chain, male_female_chain, female_female_chain)
