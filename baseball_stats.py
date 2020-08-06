import sys, os, argparse
import csv

from matplotlib import pyplot as plt

from player import Player

# USE KEYWORD ARGS FOR sort_batters and sort pitchers!
def sort_batters(reader, metric, n=float('inf'), year=2019, min_ab=0):
    """
    Sort a given number of batters in a given year by a provided metric. 
    If no number of players is provided, sort all players in the 
    provided year. If no year is provided, use the most recent year in 
    the database. Support a minimum number of ABs that defaults to 0.
    Returns a sorted list containing tuples with the player's name and 
    relevant metric.
    """
    
def sort_pitchers(reader, metric, n=float('inf'), year=2019, min_ip=0):
    """
    Sort a given number of pitchers in a given year by a provided 
    metric. If no number of players is provided, sort all players in the 
    provided year. if no year is provided, use the most recent year in
    the database. Support a minimum number of IPs that defaults to 0.
    Returns a sorted list containing tuples with the player's name and 
    relevant metric.
    """

# Represent player name as tuple (last, first)
def get_stat(reader, year, player_name, stat):
    """Get a certain stat based on the arguments provided."""
    if not name_in_dataset(player_name):
        raise ValueError
        
    return 
def get_stats(reader, year, player_name):
    """Get stats based on the arguments provided."""
    if not name_in_dataset(player_name):
        raise ValueError


    
def plot_stats(players):
    """Plot stats based on the arguments provided."""
    
def name_in_dataset(player_name):
    """Return true if the player is in the data set and false otherwise."""
    # TO BE IMPLEMENTED
    

def main():
    """Main for baseball_stats."""
    fp = os.path.dirname(__file__) + '\\data\\core\\Batting.csv'
    with open(fp) as f:
        r = csv.DictReader(f)
        for row in r:
            print(1)
    
if __name__ == '__main__':
    main()
