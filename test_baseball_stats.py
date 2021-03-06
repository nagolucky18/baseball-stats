import os
import csv
import unittest

from player import Player
import baseball_stats as bst

class PlayerTestCase(unittest.TestCase):
    """Test cases for the player class."""

    def test_in_set(self):
        """Test name_in_dataset()."""
        # Ensure return true for name in batting dataset.
        player_name = ('myers', 'wil')
        player_type = 'bat'
        in_set = bst.name_in_dataset(player_name, player_type)
        self.assertTrue(in_set)
        
        # Ensure return false for name not in batting dataset.
        bad_player_name = ('mitchell', 'ri')
        player_type = 'bat'
        in_set = bst.name_in_dataset(bad_player_name, player_type)
        self.assertFalse(in_set)
        
        # Ensure return true for name in pitching dataset.
        player_name = ('kershaw', 'clayton')
        player_type = 'pit'
        in_set = bst.name_in_dataset(player_name, player_type)
        self.assertTrue(in_set)
        
        # Ensure return false for name not in pitching dataset.
        bad_player_name = ('mitchell', 'ri')
        player_type = 'pit'
        in_set = bst.name_in_dataset(bad_player_name, player_type)
        self.assertFalse(in_set)
        
    def test_get_stat(self):
        """Test get_stat()."""
        # Ensure single stat matches for a given batter in a given year.
        year = '2015'
        player_name = ('myers', 'wil')
        player_type = 'bat'
        ps = bst.get_stat(year, player_name, player_type, '2B')
        test_ps = {'2B': '13'}
        self.assertEqual(ps, test_ps)
        
        # Ensure single stat matches for a given pitcher in a given year.
        year = '2018'
        player_name = ('ohtani', 'shohei')
        player_type = 'pit'
        ps = bst.get_stat(year, player_name, player_type, 'SO')
        test_ps = {'SO': '63'}
        self.assertEqual(ps, test_ps)
        
    def test_get_stats(self):
        """Test get_stats()."""
        # Ensure stats match for a given batter in a given year.
        year = '2015'
        player_name = ('myers', 'wil')
        player_type = 'bat'
        psa = bst.get_stats(year, player_name, player_type)
        # Hardcode invariant to ensure match.
        test_psa = {'playerID': 'myerswi01', 'yearID': '2015', 
                   'stint': '1', 'teamID': 'SDN', 'lgID': 'NL', 
                   'G': '60', 'AB': '225', 'R': '40', 'H': '57', 
                   '2B': '13', '3B': '1', 'HR': '8', 'RBI': '29', 
                   'SB': '5', 'CS': '2', 'BB': '27', 'SO': '55', 
                   'IBB': '0', 'HBP': '1', 'SH': '0', 'SF': '0', 
                   'GIDP': '2'}
        self.assertEqual(psa, test_psa)
        
        # Ensure stats match for a given pitcher in a given year.
        year = '2018'
        player_name = ('ohtani', 'shohei')
        player_type = 'pit'
        psa = bst.get_stats(year, player_name, player_type)
        # Hardcode invariant to ensure match.
        test_psa = {'playerID': 'ohtansh01', 'yearID': '2018', 
                   'stint': '1', 'teamID': 'LAA', 'lgID': 'AL', 
                   'W': '4', 'L': '2', 'G': '10', 'GS': '10', 
                   'CG': '0', 'SHO': '0', 'SV': '0', 'IPouts': '155', 
                   'H': '38', 'ER': '19', 'HR': '6', 'BB': '22', 
                   'SO': '63', 'BAOpp': '0.203', 'ERA': '3.31', 
                   'IBB': '0', 'WP': '5', 'HBP': '1', 'BK': '0',
                   'BFP': '211', 'GF': '0', 'R': '19', 'SH': '0', 
                   'SF': '1', 'GIDP': '2'}
        self.assertEqual(psa, test_psa)
        
    def test_sort_metric_only(self):
        """Test sort_batters() and sort_pitchers() using only a metric."""
        hr_leaderboard = bst.sort_batters('HR')
        hr_leader = ('alonspe', 53)
        self.assertEqual(hr_leaderboard[0], hr_leader)
        
        so_leaderboard = bst.sort_pitchers('SO')
        so_leader = ('colege0', 326)
        self.assertEqual(so_leaderboard[0], so_leader)
        
    def test_sort_n(self):
        """Test sort_batters() and sort_pitchers() with provided n."""
        hr_leaderboard = bst.sort_batters('HR', n=3)
        last_hitter = ('solerjo', 48)
        self.assertEqual(hr_leaderboard[-1], last_hitter)
        
        so_leaderboard = bst.sort_pitchers('SO', n=3)
        last_pitcher = ('biebesh', 259)
        self.assertEqual(so_leaderboard[-1], last_pitcher)
        
    def test_sort_year(self):
        """Test sort_batters() and sort_pitchers() with provided year."""
        hr_leaderboard = bst.sort_batters('HR', year='2018')
        hr_leader = ('daviskh', 48)
        self.assertEqual(hr_leaderboard[0], hr_leader)
        
        so_leaderboard = bst.sort_pitchers('SO', year='2018')
        so_leader = ('scherma', 300)
        self.assertEqual(so_leaderboard[0], so_leader)
        
    def test_sort_min(self):
        """Test sort_batters() and sort_pitchers() with a provided minimum."""
        hit_leaderboard = bst.sort_batters('H', min_ab=640)
        last_hitter = ('villajo', 176)
        self.assertEqual(hit_leaderboard[-1], last_hitter)
        
        # TEST CASE FAILS BECAUSE ADDITION OF MULTIPLE STINT METRICS
        # HAS NOT BEEN IMPLEMENTED.
        era_leaderboard = bst.sort_pitchers('ERA', min_ip=213)
        last_pitcher = ('bauertr', 4.48)
        self.assertEqual(era_leaderboard[-1], last_pitcher)
        
    def test_sort(self):
        """Test sort_batters() and sort_pitchers() with all parameters."""
        hr_leaderboard = bst.sort_batters('HR', n=3, year='2017', min_ab=650)
        last_hitter = ('gordode', 2)
        self.assertEqual(hr_leaderboard[-1], last_hitter)
        
        so_leaderboard = bst.sort_pitchers('SO', n=3, year='2016', min_ip=227)
        last_pitcher = ('priceda', 228)
        self.assertEqual(so_leaderboard[-1], last_pitcher)
    
       
unittest.main()
