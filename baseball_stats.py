import sys, os, argparse
import csv

from matplotlib import pyplot as plt

from player import Player

# USE KEYWORD ARGS FOR sort_batters and sort pitchers!
def sort_batters(metric, n=float('inf'), year=2019, min_ab=0):
    """
    Sort a given number of batters in a given year by a provided metric. 
    If no number of players is provided, sort all players in the 
    provided year. If no year is provided, use the most recent year in 
    the database. Support a minimum number of ABs that defaults to 0.
    Returns a sorted list containing tuples with the player's name and 
    relevant metric.
    """
    
def sort_pitchers(metric, n=float('inf'), year=2019, min_ip=0):
    """
    Sort a given number of pitchers in a given year by a provided 
    metric. If no number of players is provided, sort all players in the 
    provided year. if no year is provided, use the most recent year in
    the database. Support a minimum number of IPs that defaults to 0.
    Returns a sorted list containing tuples with the player's name and 
    relevant metric.
    """

# Represent player name as tuple (last, first)
def get_stat(year, player_name, player_type, stat):
    """Get a certain stat based on the arguments provided."""
    if not name_in_dataset(player_name, player_type):
        raise ValueError
        
    data = get_path(player_type)
        
    with open(data) as f:
        reader = csv.DictReader(f)
        
        lookup_name = player_name[0][0:5] + player_name[1][0:2] + '01'
        for row in reader:
            if row['playerID'] == lookup_name and row['yearID'] == year:
                    return {stat: row[stat]}
    
def get_stats(year, player_name, player_type):
    """Get stats based on the arguments provided."""
    if not name_in_dataset(player_name, player_type):
        raise ValueError
        
    data = get_path(player_type)
    
    with open(data) as f:
        reader = csv.DictReader(f)
        
        lookup_name = player_name[0][0:5] + player_name[1][0:2] + '01'
        for row in reader:
            if row['playerID'] == lookup_name and row['yearID'] == year:
                    return row
                    
def print_stats(player_name, stats):
    """
    Print the stats to the terminal. Assumes stat argument is a valid
    dictionary containing stats about the given player.
    """
    # TODO - title case player name  
    if len(stats) == 1:
        for key in stats.keys():
            print('{0} stat for {1}, {2}: {3}'.format(key, 
            player_name[0].title(), player_name[1].title(), stats[key]))
    else:
        print('Stats for {0}, {1}:'.format(player_name[0].title(), 
            player_name[1].title()))
        for key in stats.keys():
            print('{0}: {1}'.format(key, stats[key]))
                
def plot_stats(players):
    """Plot stats based on the arguments provided."""
    
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
    
def main():
    """Main for baseball_stats."""
    pn = ('myers', 'wil')
    print_stats(pn, (get_stats('2015', pn, 'bat')))
    
    pn_2 = ('ohtani', 'shohei')
    print_stats(pn_2, (get_stat('2018', pn_2, 'pit', 'SO')))
    
if __name__ == '__main__':
    main()
