import os
import csv
import unittest

from player import Player
from baseball_stats import get_stat, get_stats, name_in_dataset

class PlayerTestCase(unittest.TestCase):
    """Test cases for the player class."""

    def test_in_set(self):
        """Test name_in_dataset()."""
        # Ensure return true for name in batting dataset.
        player_name = ('myers', 'wil')
        player_type = 'bat'
        in_set = name_in_dataset(player_name, player_type)
        self.assertTrue(in_set)
        
        # Ensure return false for name not in batting dataset.
        bad_player_name = ('mitchell', 'ri')
        player_type = 'bat'
        in_set = name_in_dataset(bad_player_name, player_type)
        self.assertFalse(in_set)
        
        # Ensure return true for name in pitching dataset.
        player_name = ('kershaw', 'clayton')
        player_type = 'pit'
        in_set = name_in_dataset(player_name, player_type)
        self.assertTrue(in_set)
        
        # Ensure return false for name not in pitching dataset.
        bad_player_name = ('mitchell', 'ri')
        player_type = 'pit'
        in_set = name_in_dataset(bad_player_name, player_type)
        self.assertFalse(in_set)
        
    def test_get_stat(self):
        """Test get_stat()."""
        # Ensure single stat matches for a given batter in a given year.
        year = '2015'
        player_name = ('myers', 'wil')
        player_type = 'bat'
        ps = get_stat(year, player_name, player_type, '2B')
        test_ps = {'2B': '13'}
        self.assertEqual(ps, test_ps)
        
        # Ensure single stat matches for a given pitcher in a given year.
        year = '2018'
        player_name = ('ohtani', 'shohei')
        player_type = 'pit'
        ps = get_stat(year, player_name, player_type, 'SO')
        test_ps = {'SO': '63'}
        self.assertEqual(ps, test_ps)
        
    def test_get_stats(self):
        """Test get_stats()."""
        # Ensure stats match for a given batter in a given year.
        year = '2015'
        player_name = ('myers', 'wil')
        player_type = 'bat'
        psa = get_stats(year, player_name, player_type)
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
        psa = get_stats(year, player_name, player_type)
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
        
            
unittest.main()
