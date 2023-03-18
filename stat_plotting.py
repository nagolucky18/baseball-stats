from matplotlib import pyplot as plt

from stat_sorting import *
from query import *

# Try setting same number of bins to make bar width consistent across
# all metrics!
def plot_metric_stats(player_type, year, metric, n, minimum):
    """Plot stats based on the arguments provided."""
    
    incr_values_b = {'G': 20, 'AB': 50, 'R': 10, 'H': 20, '2B': 5, 
                     '3B': 1, 'HR': 5, 'RBI': 10, 'BB': 10, 'SO': 20,
                     'IBB': 2, 'HBP': 2, 'SH': 2, 'SF': 1, 'GIDP': 2}
    
    # SH and SF not currently supported. Database must be manually evaluated.
    incr_values_p = {'W': 2, 'L': 2, 'G': 10, 'GS': 3, 'CG': 1, 'SHO': 1,
                     'SV': 4, 'IPouts': 100, 'H': 20, 'ER': 10, 'HR': 4, 
                     'BB': 10, 'SO': 30, 'BAOpp': 0.05, 'ERA': 0.5, 
                     'IBB': 1, 'WP': 2, 'HBP': 2, 'BK': 1, 'BFP': 100,
                     'GF': 5, 'R': 10, 'SH': 0, 'SF': 0, 'GIDP': 3}
    
    if player_type == 'bat':
        stats = sort_batters(metric, n, minimum, year)
        # incr_value = incr_values_b[metric]
    elif player_type == 'pit':
        stats = sort_pitchers(metric, n, minimum, year, True)
        # incr_value = incr_values_p[metric]
    else:
        raise ValueError
    """
    if incr_value < 1:
        w = 0.35
    elif incr_value < 5:
        w = 1
    elif incr_value < 10:
        w = 3
    else:
        w = 4
    """
    
    stats.reverse()
    
    values = [stats[i][1] for i in range(0, len(stats))]
    groups = []
    if metric == 'ERA':
        max_val = 6.0
    else:
        max_val = stats[-1][1]
        
    if metric == 'ERA':
        incr_val = 0.6
    else:
        incr_val = max_val // 10

    grp_val = 0
    i = 0
    while grp_val < max_val:
        cv = 0
        while i < len(values) and values[i] < (grp_val+incr_val):
            cv += 1
            i += 1
        groups.append(cv)
        grp_val += incr_val
    
    if metric == 'ERA' or metric == 'BAopp':
        x_labels = []
        i = 0
        while i < max_val:
            x_labels.append(round(i,2))
            i += incr_val
    else:
        x_labels = [i for i in range(0, max_val, incr_val)]
        
    if metric == 'ERA':
        w = max_val / 10
    else:
        w = max_val // 10
    
    plt.bar(x_labels, groups, width=w, tick_label=x_labels,
                edgecolor=(0,0,0), linewidth=1)
    
    if player_type == 'bat': 
        min_str = 'min ab = '
    elif player_type == 'pit':
        min_str = 'min ip = '
    title = metric + ', ' + year + ', ' + min_str + str(minimum)
    plt.title(title, fontsize=24)
    plt.xlabel('Total ' + metric, fontsize=12)
    plt.ylabel('Number of players', fontsize=12)
    
    plt.show()