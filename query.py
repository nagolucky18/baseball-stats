import os
import csv

def name_in_dataset(player_name, player_type):
    """Return true if the player is in the data set and false otherwise."""
    data = get_path(player_type)
    
    with open(data) as f:
        reader = csv.DictReader(f)
        
        lookup_name = player_name[0][0:5] + player_name[1][0:2] + '01'
        for row in reader:
            if row['playerID'] == lookup_name:
                return True
        return False
        
def get_path(query):
    """Return the requested file based on the query."""
    # Support for other data sets to be implemented at later date.
    if query == 'bat':
        ds = os.path.dirname(__file__) + '\\data\\core\\Batting.csv'
    elif query == 'pit':
        ds = os.path.dirname(__file__) + '\\data\\core\\Pitching.csv'
    else:
        raise ValueError
    
    return ds