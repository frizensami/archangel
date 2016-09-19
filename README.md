# tAngel 2016: Matching algorithm
## Author: Sriram Sami

### Overview
This year's algorithm uses a Hamiltonian-cycle based approach to finding valid angel-mortal chains. Critically, `networkx` was used for graph algorithms.

### Usage
1. Clone the repo
2. Create a virtual environment so that the required libraries don't pollute your namespace (Optional). Run `virtualenv venv` in the cloned directory.
3. Install requirements with `pip install -r requirements.txt`
4. Put a header-less tsv file (no column names, the first row is the first row of data already) with all details of participants in correct order in a file called `playerlist.tsv` in the main folder.
5. Run `python angel.py`


### Columns required for playerlist.tsv
The columns in playerlist.tsv should be arranged as such, with 1 being the leftmost column. Important columns for matching: 2, 4, 7, 9, 10.


1. Timestamp
2. Full Name
3. Facebook Name (if different)
4. Floor Number
5. Room Number
6. Contact Number
7. Gender
8. Year of Study
9. What's your gender preference for your Angel and Mortal?
10. Faculty 
11. Interests
12. Is there anything that you'd like us to know?                                                       
