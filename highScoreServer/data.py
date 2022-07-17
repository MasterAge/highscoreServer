from json import JSONEncoder
from typing import Dict

import geocoder


class Player:
    """A player who submits a highscore"""

    def __init__(self, username: str, score: int, ip_addr: str = None, location: str = None) -> None:
        super().__init__()
        self.username = username
        self.score = score

        if location:
            self.location = location
        elif ip_addr:
            self.location = geocoder.ip(ip_addr).country or ""
        else:
            self.location = ""


class PlayerEncoder(JSONEncoder):
    """Encodes a player object into a JSON object."""
    def default(self, o: Player):
        return o.__dict__


class Datastore:

    def init(self):
        """Setup required resources."""
        pass

    def update_score(self, new_player: Player):
        """
        Updates a player's score.
        If the player does not exist, the player is added to the database.
        :param new_player: The player
        """
        player = self.get_player(new_player.username)

        if not player:
            self.create_player(new_player)
        elif player.score < new_player.score:
            self.update_player_score(new_player.username, new_player.score)

    def get_scores(self, start, count) -> list:
        """
        Get a list of player scores
        :param start: The starting index from highest score.
        :param count: The amount of score to retrieve
        :return: A list of player scores
        """
        pass

    def get_player(self, username) -> Player:
        """
        Get a player object from their username.
        :param username: The player's username
        :return: The player
        """
        pass

    def create_player(self, new_player: Player):
        """
        Create a new player assuming ones does not exist.

        :param new_player: Player details.
        """
        pass

    def update_player_score(self, player_name: str, score: int):
        """
        Update the score of a player in the datastore.
        :param player_name: Name of player.
        :param score: Player's new score
        """
        pass


class InMemoryDatastore(Datastore):
    """A datastore that is purely in-memory."""
    scores: Dict[str, Player] = dict()

    def create_player(self, new_player: Player):
        self.scores[new_player.username] = new_player

    def update_player_score(self, player_name: str, score: int):
        self.scores[player_name].score = score

    def get_scores(self, start, count) -> list:
        return sorted(self.scores.values(), key=lambda player: player.score, reverse=True)[start:count]

    def get_player(self, username) -> Player:
        return self.scores.get(username)
