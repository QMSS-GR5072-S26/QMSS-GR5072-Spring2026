import pytest
#from hearts import HeartsGame
from hearts_fixed import HeartsGame

def test_round_score_unbiased():
    """Over many rounds, each player should receive similar total hearts"""
    game = HeartsGame()
    totals = [0] * 4
    for _ in range(10000):
        scores = game.round_score()
        for i, s in enumerate(totals):
            totals[i] += scores[i]
    # Each player should have roughly 25% of total hearts
    for total in totals:
        #self.assertAlmostEqual(total / sum(totals), 0.25, delta=0.02)
        assert total / sum(totals) == pytest.approx(0.25, abs=0.02)

