from json import JSONEncoder

import geocoder


class Player:
    def __init__(self, username, score, ip_addr) -> None:
        super().__init__()
        self.username = username
        self.score = int(score)
        self.location = geocoder.ip(ip_addr).country


class PlayerEncoder(JSONEncoder):
    def default(self, o: Player):
        return o.__dict__


class Datastore:
    scores = dict()

    def update_score(self, new_player: Player):
        player = self.scores.get(new_player.username)

        if not player:
            self.scores[new_player.username] = new_player
        elif player.score < new_player.score:
            player.score = new_player.score

    def get_scores(self, start, count) -> list:
        sorted_scores = sorted(self.scores.values(), key=lambda player: player.score, reverse=True)[start:count]
        return sorted_scores

    def get_player(self, username):
        return self.scores.get(username)
