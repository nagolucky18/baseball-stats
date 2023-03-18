from operator import itemgetter

from query import *

def sort_batters(metric, n='A', min_ab=0, year='', r=True):
    """
    Sort a given number of batters in a given year by a provided metric. 
    If no number of players is provided, sort all players in the 
    provided year. If no year is provided, use the most recent year in 
    the database. Support a minimum number of ABs that defaults to 0.
    Returns a sorted list containing tuples with the player's name and 
    relevant metric.
    """
    if n == 'A':
        n = float('inf');
        
    data = get_path('bat')
    
    batters = []
    
    with open(data) as f:
        reader = csv.DictReader(f)
        
        if year == '':
            year = '2020'
        
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
                if int(row['AB']) >= min_ab and repeat_player == False:
                    batters.append((pID, val))   
           
    sb = sorted(batters, key=itemgetter(1), reverse=r)
    
    if n < len(batters):
        return sb[:n]
    else:
        return sb
    
def sort_pitchers(metric, n='A', min_ip=0, year='', r=False):
    """
    Sort a given number of pitchers in a given year by a provided 
    metric. If no number of players is provided, sort all players in the 
    provided year. if no year is provided, use the most recent year in
    the database. Support a minimum number of IPs that defaults to 0.
    Returns a sorted list containing tuples with the player's name and 
    relevant metric.
    """
    if n == 'A':
        n = float('inf');
        
    min_ip *= 3
    if metric == 'SO' or metric == 'W' or metric == 'GIDP':
        r = True
    
    data = get_path('pit')
    
    pitchers = []
    
    with open(data) as f:
        reader = csv.DictReader(f)
        
        if year == '':
            year = '2020'
        
        for row in reader:
            if row['yearID'] == year:
                repeat_player = False
                pID = row['playerID'][0:7]
                if row['playerID'][-2:] != '01':
                    pID = row['playerID']
                if metric != 'ERA' and metric != 'BAOpp':
                    val = int(row[metric])
                else:
                    if row[metric] != '':
                        if metric == 'ERA':
                            val = (int(row['ER']), int(row['IPouts']))
                        
                ip = int(row['IPouts'])
                
                # Check to see whether the stats quantify stats from
                # a players additional stints.
                for i in range(len(pitchers)):
                    if pitchers[i][0] == pID:
                        if metric != 'ERA' and metric != 'BAOpp':
                            n_val = pitchers[i][1] + val
                        else:
                            # Averaging ERA does not work this way.
                            n_val = (pitchers[i][1][0] + int(row['ER']), 
                                pitchers[i][1][1] + int(row['IPouts']))
                            ip += pitchers[i][2]
                        pitchers[i] = (pID, n_val, ip)
                        repeat_player = True
                        
                if repeat_player == False:
                    pitchers.append((pID, val, ip))   
                    
    # Lengthy and confusing implementation -> trim down if possible.
    if metric == 'ERA':
        for i in range(len(pitchers)):
            pitchers[i] = (pitchers[i][0], round((((pitchers[i][1][0]*3)/pitchers[i][1][1]) * 9),2), pitchers[i][2])
    
    i = 0
    while i < len(pitchers):
        if pitchers[i][2] < min_ip:
            pitchers.remove(pitchers[i]);
            continue
        pitchers[i] = (pitchers[i][0], pitchers[i][1])
        i += 1
           
    sp = sorted(pitchers, key=itemgetter(1), reverse=r)
    
    if n < len(pitchers):
        return sp[:n]
    else:
        return sp
        
def sort_players(player_type, year, metric, n, minimum):
    """Sort players according to the player_type provided."""
    if player_type == 'bat':
        return sort_batters(metric, int(n), int(minimum), year)
    elif player_type == 'pit':
        return sort_pitchers(metric, int(n), int(minimum), year)