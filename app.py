import json

from flask import Flask, request, abort, url_for

from data import Datastore, Player, PlayerEncoder

app = Flask(__name__)
datastore = Datastore()


# GET /highscores get all scores
# GET /highscores?start_rank&count
@app.route('/highscore')
def get_all_scores(start=0, count=10):
    return json.dumps(datastore.get_scores(start, count), cls=PlayerEncoder)


# POST /highscore submit a new score
@app.route('/highscore', methods=['POST'])
def submit_score():
    body = request.json
    player = Player(body['username'], body['score'], request.remote_addr)
    datastore.update_score(player)
    return url_for('get_player', username=player.username)


# GET /highscore/username
@app.route('/highscore/<username>', methods=['GET'])
def get_player(username):
    player = datastore.get_player(username)
    if player:
        return json.dumps(player, cls=PlayerEncoder)
    else:
        abort(404)


if __name__ == '__main__':
    app.run()
