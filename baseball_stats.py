import sys, os, argparse
from operator import itemgetter
import csv

from matplotlib import pyplot as plt

from player import Player

# USE KEYWORD ARGS FOR sort_batters and sort pitchers!

# TODO - factor in abs, ips for multiple stints

def sort_batters(metric, n=float('inf'), year="2019", min_ab=0, 
                 r=True):
    """
    Sort a given number of batters in a given year by a provided metric. 
    If no number of players is provided, sort all players in the 
    provided year. If no year is provided, use the most recent year in 
    the database. Support a minimum number of ABs that defaults to 0.
    Returns a sorted list containing tuples with the player's name and 
    relevant metric.
    """
    if metric == 'GIDP':
        r = False
        
    data = get_path('bat')
    
    batters = []
    
    with open(data) as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            if row['yearID'] == year:
                repeat_player = False
                pID = row['playerID'][0:7]
                val = int(row[metric])
                for i in range(len(batters)):
                    if batters[i][0] == pID:
                        n_val = batters[i][1] + val
                        batters[i] = (pID, n_val)
                        repeat_player = True
                if int(row['AB']) > min_ab and repeat_player == False:
                    batters.append((pID, val))   
           
    sb = sorted(batters, key=itemgetter(1), reverse=r)
    
    if n < len(batters):
        return sb[:n]
    else:
        return sb
    
def sort_pitchers(metric, n=float('inf'), year="2019", min_ip=0,
                  r=False):
    """
    Sort a given number of pitchers in a given year by a provided 
    metric. If no number of players is provided, sort all players in the 
    provided year. if no year is provided, use the most recent year in
    the database. Support a minimum number of IPs that defaults to 0.
    Returns a sorted list containing tuples with the player's name and 
    relevant metric.
    """
    min_ip *= 3
    if metric == 'SO':
        r = True
    
    data = get_path('pit')
    
    pitchers = []
    
    with open(data) as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            if row['yearID'] == year:
                repeat_player = False
                pID = row['playerID'][0:7]
                if metric != 'ERA' and metric != 'BAOpp':
                    val = int(row[metric])
                else:
                    if row[metric] != '':
                        val = float(row[metric])
                for i in range(len(pitchers)):
                    if pitchers[i][0] == pID:
                        if metric != 'ERA' and metric != 'BAOpp':
                            n_val = pitchers[i][1] + val
                        else:
                            n_val = (pitchers[i][1] + val) / 2
                        pitchers[i] = (pID, n_val)
                        repeat_player = True
                if int(row['IPouts']) > min_ip and repeat_player == False:
                    pitchers.append((pID, val))   
           
    sp = sorted(pitchers, key=itemgetter(1), reverse=r)
    
    if n < len(pitchers):
        return sp[:n]
    else:
        return sp
    
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
                
def plot_metric_stats(player_type, metric, n=float('inf'), year="2019", min_ab=0):
    """Plot stats based on the arguments provided."""
    
    incr_values_b = {'G': 20, 'AB': 50, 'R': 10, 'H': 20, '2B': 5, 
                     '3B': 1, 'HR': 5, 'RBI': 10, 'BB': 10, 'SO': 20,
                     'IBB': 2, 'HBP': 2, 'SH': 2, 'SF': 1, 'GIDP': 2}
    
    if player_type == 'bat':
        stats = sort_batters(metric, n, year, min_ab, r=False)
        incr_value = incr_values_b[metric]
    elif player_type == 'pit':
        stats = sort_batters(metric, n, year, min_ab, r=False)
    else:
        raise ValueError
    
    if incr_value < 5:
        w = 1
    elif incr_value < 10:
        w = 3
    else:
        w = 4

    values = [stats[i][1] for i in range(0, len(stats))]
    groups = []
    max_val = stats[-1][1]
    grp_val = 0
    i = 0
    while grp_val < max_val:
        cv = 0
        while i < len(values) and values[i] < (grp_val+incr_value):
            cv += 1
            i += 1
        groups.append(cv)
        grp_val += incr_value
        
    x_labels = [i for i in range(0, max_val, incr_value)]
    
    plt.bar(x_labels, groups, width=w, tick_label=x_labels)
    
    title = metric + ', ' + year
    plt.title(title, fontsize=24)
    plt.xlabel('Total ' + metric, fontsize=12)
    plt.ylabel('Number of players', fontsize=12)
    
    plt.show()
    
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
    plot_metric_stats('bat', 'RBI')
    
if __name__ == '__main__':
    main()
