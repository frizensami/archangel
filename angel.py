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

# GLOBALS
PLAYERFILE = "playerlist.csv"


class Player:
        def is_valid(self):
                return self.name != "" and self.floor != "" and self.room_number != ""

        def __init__(self, **kwargs):
                self.name = kwargs.get('name')
                self.fbname = kwargs.get('fbname')
                self.floor = kwargs.get('floor')
                self.room_number = kwargs.get('room_number')
                self.gender = kwargs.get('gender')
                self.year = kwargs.get('year')
                self.gender_pref = kwargs.get('gender_pref')
                self.faculty = kwargs.get('faculty')
                self.interests = kwargs.get('interests')

        def __repr__(self):
                return str(self.name) + ": " + str(self.floor) + "-" + str(self.room_number)


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

if __name__ == "__main__":
        print ""
        print ""
        print "============================================="
        print "tAngel 2016 engine initializing.............."
        print "============================================="
        print ""
        print ""
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


