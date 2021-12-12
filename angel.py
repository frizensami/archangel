'''
tAngel angel-mortal matching code
Author: Sriram Sami + Elgene 2021 update
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
import logging
import datetime
# # FROMS
from models import Player
from arrange import angel_mortal_arrange

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=f'logs/{datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")}.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)




# GLOBALS
PLAYERFILE = "playerlist.csv"

# Constants
GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_NONBINARY = "non-binary"
GENDER_NOPREF = "no preference"

GENDER_SWAP_PREFERENCE_PERCENTAGE = 0.0 #100 if you wanna change all players with no gender pre to have genderpref = opposite gender, 0 if you wanna all to remain as no geneder pref




def read_csv(filename):
    person_list = []
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                logger.info(f'Column names are {", ".join(row)}')
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                playerUsername=row[0].strip().lower()
                playerName=row[1].strip().lower()
                genderPref = row[2].strip().lower()
                genderPlayer = row[3].strip().lower()
                interests = row[4].strip()
                twotruthsonelie = row[5].strip()
                introduction = row[6].strip()
                houseNumber = row[7].strip().lower()
                CGnumber = row[8].strip().lower()
                yearofStudy = row[9].strip().lower()
                faculty = row[10].strip().lower()

                new_person = Player(username = playerUsername,
                    playername = playerName,
                    genderpref=genderPref,
                    genderplayer=genderPlayer,
                    interests=interests,
                    twotruthsonelie=twotruthsonelie,
                    introduction=introduction,
                    housenumber = houseNumber,
                    cgnumber = CGnumber,
                    yearofstudy = yearofStudy,
                    faculty = faculty,
                    )
                person_list.append(new_person)
                logger.info(f'Adding ' + str(new_person))
                print(f'Adding ' + str(new_person))
                line_count += 1
        print (f'Processed {line_count} lines.')
        logger.info(f'Processed {line_count} lines.')
        logger.info(f'person_list has been processed successfully')
    return person_list





def separate_players(player_list):
    '''
    Separates the list of player list into male_male, male_female, and
    female_female gender preference lists

    CURRENTLY USELESS FUNCTION
    '''
    male_male_list = []
    male_female_list = []
    female_female_list = []

    for player in player_list:
        if (player.genderplayer == 'male' and player.genderpref == 'male') or (player.genderplayer == "non-binary" and player.genderpref == "male"):
            male_male_list.append(player)
            print(f'Added Player: {player.username}, Gender: {player.genderplayer}, GenderPref: {player.genderpref} to male_male_list')
            logger.info(f'Added Player: {player.username}, Gender: {player.genderplayer}, GenderPref: {player.genderpref} to male_male_list')
        elif (player.genderplayer == 'female' and player.genderpref == 'female') or (player.genderplayer == "non-binary" and player.genderpref == "female"):
            female_female_list.append(player)
            print(f'Added Player: {player.username}, Gender: {player.genderplayer}, GenderPref: {player.genderpref} to female_female_list')
            logger.info(f'Added Player: {player.username}, Gender: {player.genderplayer}, GenderPref: {player.genderpref} to female_female_list')
        else:
            male_female_list.append(player)
            print(f'Added Player: {player.username}, Gender: {player.genderplayer}, GenderPref: {player.genderpref} to male_female_list')
            logger.info(f'Added Player: {player.username}, Gender: {player.genderplayer}, GenderPref: {player.genderpref} to male_female_list')
    return (male_male_list, male_female_list, female_female_list)


'''
savegenderlist is unused
'''
def savegenderlist(genderlist: list):
    temp = []
    for k, v in players.items():
        temp[k] = v.genderplayer
        temp[k] = v.genderpref

    with open(genderlist.json, 'w+') as f:
        json.dump(temp, f)

playerList = read_csv("playerlist.csv")

gendermatchinglist = separate_players(playerList)
# savegenderlist(male_male_list)


def modify_player_list(player_list):
    # Force hetero mix
    for player in player_list:
        if player.genderpref == GENDER_NOPREF:
            random_change_preference = random.random() < GENDER_SWAP_PREFERENCE_PERCENTAGE
            if player.genderplayer == GENDER_MALE and random_change_preference:
                print (f"Male -> Female")
                player.genderpref = GENDER_FEMALE
            elif player.genderplayer == GENDER_FEMALE and random_change_preference:
                print (f"Female -> Male")
                player.genderpref = GENDER_MALE


def write_to_csv(index, name01, *player_lists):
    '''
    Writes a variable number of player lists to csv
    '''
    for player_list in player_lists:
        if player_list is not None:
            print (f"Length of list: {len(player_list)}")
            cur_time = time.strftime("%Y-%m-%d %H-%M-%S")
            with open(f"{index} - {name01} - {cur_time}.csv", 'w', newline='') as f: ##In Python 3, if do not put newline='' AND choose 'w' instead of 'wb', you will have an empty 2nd row in output .csv file.
                writer = csv.writer(f, delimiter=',')
                header = ['Telegram Username','Name','GenderPref','Gender','Interests','2truths1lie','Intro','House','CG','Year','Faculty'] ##add header to output csv file
                writer.writerow(i for i in header)
                for player in player_list:
                    if '\n' in player.twotruthsonelie:
                        string1 = player.twotruthsonelie
                        string2 = string1.replace('"', "'")  ##JUST IN CASE PEOPLE TYPE " which can screw up a csv file
                        string3 = ''.join(('"', string2,'"'))  ##Double quotations are what CSV uses to keep track of newlines within the same cell
                        player.twotruthsonelie = string3

                    if '\n' in player.interests:
                        string11 = player.interests
                        string12 = string11.replace('"', "")  ##JUST IN CASE PEOPLE TYPE " which can screw up a csv file
                        string13 = ''.join(('"', string12,'"'))  ##Double quotations are what CSV uses to keep track of newlines within the same cell
                        player.interests = string13

                    if '\n' in player.introduction:
                        string21 = player.introduction
                        string22 = string21.replace('"',"'")  ##JUST IN CASE PEOPLE TYPE " which can screw up a csv file
                        string23 = ''.join(('"', string22,'"'))  ##Double quotations are what CSV uses to keep track of newlines within the same cell
                        player.introduction = string23

                    f.write(player.to_csv_row())
                    f.write("\n")
            # # write the first player again to close the loop
            #     f.write(player_list[0].to_csv_row())
            #     f.write("\n")
                f.close()

def Difference_operator_lists(li1, li2):  ##Used to find out the rejected players
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

if __name__ == "__main__":
    print (f"\n\n")
    print (f"=============================================")
    print (f"tAngel 2021 engine initializing..............")
    print (f"=============================================")
    print (f"\n\n")

    # Get list of Player objects from csv file
    player_list = read_csv(PLAYERFILE)
    # Map the player list through any neccessary transformations
    modify_player_list(player_list)
    # separate the players into player-chains (connected components)
    list_of_player_chains = angel_mortal_arrange(player_list)
    # Write each chain to a separate csv
    print("done")
    for index, player_chain in enumerate(list_of_player_chains):
        write_to_csv(index, "accepted", player_chain)
        # creating csv list of rejected players
        rejected_players_list = Difference_operator_lists(player_list, player_chain)
        if len(rejected_players_list) == 0:
            print("rejected players list is empty")
        else:
            write_to_csv(index, "rejected", rejected_players_list)
            print("rejected players list csv created")
