import unittest
import numpy as np
import hearts_fixed 

class TestPlayer(unittest.TestCase):
    
    def setUp(self):
        """Create a fresh player before each test"""
        self.player = hearts_fixed.Player(0)
    
    def test_initial_state(self):
        """Player should start with zero score and wins"""
        self.assertEqual(self.player.score, 0)
        self.assertEqual(self.player.games_won, 0)
        self.assertEqual(self.player.player_id, 0)
    
    def test_add_score(self):
        """add_score should accumulate points"""
        self.player.add_score(10)
        self.assertEqual(self.player.score, 10)
        self.player.add_score(5)
        self.assertEqual(self.player.score, 15)
    
class TestHeartsGame(unittest.TestCase):
    
    def setUp(self):
        """Create a fresh game before each test"""
        self.game = hearts_fixed.HeartsGame()
    
    # --- Initialization tests ---
    def test_initial_players(self):
        """Game should start with 4 players"""
        self.assertEqual(len(self.game.players), 4)
    
    def test_initial_rounds(self):
        """Game should start with 0 rounds played"""
        self.assertEqual(self.game.rounds_played, 0)
    
    def test_players_are_player_objects(self):
        """Each player should be a Player instance"""
        for player in self.game.players:
            self.assertIsInstance(player, hearts_fixed.Player)

    def test_round_score_non_negative(self):
        """round_score should never return negative scores"""
        for _ in range(100):
            scores = self.game.round_score()
            for score in scores:
                self.assertGreaterEqual(score, 0)

    # --- play_round tests ---
    def test_play_round_increments_rounds(self):
        """play_round should increment rounds_played"""
        self.game.play_round()
        self.assertEqual(self.game.rounds_played, 1)
    
    # --- get_winners tests ---
    def test_get_winners_returns_lowest_score(self):
        """get_winners should return player(s) with lowest score"""
        self.game.players[0].add_score(10)
        self.game.players[1].add_score(5)   # lowest
        self.game.players[2].add_score(15)
        self.game.players[3].add_score(20)
        winners = self.game.get_winners()
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0].player_id, 1)
    
    def test_get_winners_handles_tie(self):
        """get_winners should return all tied players"""
        self.game.players[0].add_score(5)
        self.game.players[1].add_score(5)
        self.game.players[2].add_score(15)
        self.game.players[3].add_score(20)
        winners = self.game.get_winners()
        self.assertEqual(len(winners), 2)

    # --- play tests ---
    
    def test_play_points_exceeds_threshold(self):
        """play with points should stop when a player exceeds threshold"""
        self.game.play("points", 50)
        self.assertTrue(any(p.score >= 50 for p in self.game.players))
   
    def test_play_resets_between_games(self):
        """scores should reset between games but wins should persist"""
        self.game.play("rounds", 5)
        wins_after_first = [p.games_won for p in self.game.players]
        self.game.play("rounds", 5)
        # wins should have grown
        wins_after_second = [p.games_won for p in self.game.players]
        self.assertGreater(sum(wins_after_second), sum(wins_after_first))

    # --- bias test  ---
    def test_round_score_unbiased(self):
        """Over many rounds, each player should receive similar total points"""
        totals = [0] * 4
        for _ in range(5000):
            scores = self.game.round_score()
            for i, score in enumerate(scores):
                totals[i] += score
        total_points = sum(totals)
        for total in totals:
            self.assertAlmostEqual(total / total_points, 0.25, delta=0.05)

class TestIntegration(unittest.TestCase):
    def setUp(self):
        """Create a fresh player before each test"""
        self.player = hearts_fixed.Player(0)
        self.game = hearts_fixed.HeartsGame()
 
    def test_play_round_integration(self):
        """
        Integration test: round_score() output flows correctly 
        through play_round() into Player.add_score()
        """
        # Record scores before
        scores_before = [p.score for p in self.game.players]
        
        # Run play_round -- which calls round_score() and add_score()
        self.game.play_round()
        
        # Record scores after
        scores_after = [p.score for p in self.game.players]
        
        # The difference should sum to 26
        differences = [after - before for after, before 
                       in zip(scores_after, scores_before)]
        self.assertEqual(sum(differences), 26)
        
        # Each player's score should have increased or stayed same
        for diff in differences:
            self.assertGreaterEqual(diff, 0)
        
        # rounds_played should have incremented
        self.assertEqual(self.game.rounds_played, 1)

if __name__ == '__main__':
    unittest.main(argv=['verbose'], verbosity=2,exit=False)