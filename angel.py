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
- Achieved by separating by HOUSE (floor) and 


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
PLAYERFILE="playerlist.csv"
 
def read_csv(filename):
        '''
        Reads a CSV file and outputs a list of Player objects
        '''
        pass

if __name__ == "__main__":
        print "tAngel 2016 engine initialization starting..."
        player_list = read_csv(PLAYERFILE)


        




