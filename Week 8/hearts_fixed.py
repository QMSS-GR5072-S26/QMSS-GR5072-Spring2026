import numpy as np
import time

rng = np.random.default_rng()

# --- Player Class ---
class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.score = 0
        self.games_won = 0

    def add_score(self, points):
        self.score += points

    def reset_score(self):
        self.score = 0

    @property
    def is_winning(self):
        """Can be checked externally against other players"""
        return self.score  # lower is better in Hearts

    def __repr__(self):
        return f"Player {self.player_id} | Score: {self.score} | Wins: {self.games_won}"


# --- HeartsGame Class ---
class HeartsGame:
    def __init__(self):
        self.players = [Player(i) for i in range(4)]
        self.rounds_played = 0

    def round_score(self):
        """Simulate one round of Hearts"""
        scores = []
        remaining = 13
        scores = [0] * 4
        shuffle_list = rng.permutation(4).tolist()
        for i, player in enumerate(shuffle_list):
            if i < 3:
                score = rng.integers(0, remaining, endpoint=True)
                scores[player] = score  # assign to correct player index
                remaining -= score
            else:
                scores[player] = remaining
        queen = rng.integers(0, 3, endpoint=True)
        scores[queen] += 13
        return scores

    def play_round(self):
        """Apply one round's scores to players"""
        new_scores = self.round_score()
        for player, score in zip(self.players, new_scores):
            player.add_score(score)
        self.rounds_played += 1

    def get_winners(self):
        """Return player(s) with the lowest score"""
        min_score = min(p.score for p in self.players)
        return [p for p in self.players if p.score == min_score]

    def reset(self):
        """Reset for a new game"""
        for player in self.players:
            player.reset_score()
        self.rounds_played = 0

    def play(self, gametype, endvalue):
        """Main game loop"""
        self.reset()

        if gametype == "points":
            while all(p.score < endvalue for p in self.players):
                self.play_round()

        elif gametype == "rounds":
            for _ in range(endvalue):
                self.play_round()

        winners = self.get_winners()
        for w in winners:
            w.games_won += 1

        player_list = ', '.join(str(w.player_id) for w in winners)
        label = "winner is player" if len(winners) == 1 else "winners are players"
        #print(f"Yay! The {label} {player_list} after {self.rounds_played} rounds")
        #print(', '.join(str(p.score) for p in self.players))
        #print("Standings:", self.players)