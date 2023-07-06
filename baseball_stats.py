import sys, os, argparse

from player import Player
from stat_sorting import *
from stat_plotting import *
from query import *

# USE KEYWORD ARGS FOR sort_batters and sort pitchers!

# TODO - factor in abs, X - ips for multiple stints
#      X - differentiate between players with same name
#      - fixed bar width for chart

# Represent player name as tuple (last, first)
def get_stat(player_type, year, player_name, stat):
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
    
def get_stats(player_type, year, player_name):
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
    
# TODO - add playerstat, playerstats arguments -> remove defaults 
# for all functions.
def main():
    """Main for baseball_stats."""
    desc_str = """
    This program accepts command line input and outputs 
    desired baseball statistics.
    
    Argument Formatting:
    
    YEAR: year
    PLAYERTYPE: "bat" or "pit"
    PLAYERNAME: lastname,firstname
    STAT: stat {SEE STATS SUPPORTED}
    TOTALPLAYERS: total players, use "A" for all players
    MINIMUM: minimum
    """
  
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc_str)

    parser.add_argument('--playerstat', nargs=4, metavar=('PLAYERTYPE', 
        'YEAR', 'PLAYERNAME', 'STAT'))
    parser.add_argument('--playerstats', nargs=3, metavar=('PLAYERTYPE',
        'YEAR', 'PLAYERNAME'))
    parser.add_argument('--rank', nargs=5, metavar=('PLAYERTYPE', 
        'YEAR', 'STAT', 'TOTALPLAYERS', 'MINIMUM'))
    parser.add_argument('--graph', nargs=5, metavar=('PLAYERTYPE',
        'YEAR', 'STAT', 'TOTALPLAYERS', 'MINIMUM'))
    
    args = parser.parse_args()
    
    # Catch the value error raised if a player is not in the dataset. There is currently
    # an issue if two players share a last name AND share the first two characters of a
    # first name.
    try:
        if args.playerstat:
            args.playerstat[2] = args.playerstat[2].split(',');
            print(get_stat(*args.playerstat))
        elif args.playerstats:
            args.playerstats[2] = args.playerstats[2].split(',');
            print(get_stats(*args.playerstats))
        elif args.rank:
            print(sort_players(*args.rank))
        elif args.graph:
            if args.graph[3] == 'A':
                args.graph[3] = float('inf')
            else:
                args.graph[3] = int(args.graph[3])
            args.graph[4] = int(args.graph[4])
            print(plot_metric_stats(*args.graph))
        else:
            print('Improper usage. For help, use baseball_stats.py -h')
    except ValueError:
        print('Name not in dataset.')
    
if __name__ == '__main__':
    main()
