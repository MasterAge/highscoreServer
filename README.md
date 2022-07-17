# High Score Server
A flask based high score server for game jams.

## Setup
```bash
pip install -r requirements.txt
```

## Run
```bash
FLASK_APP="highScoreServer/app.py" FLASK_ENV="release" FLASK_DEBUG="0" python -m flask run
```

This will start a sever at http://127.0.0.1:5000

## Endpoints
See [tests.http](./tests.http) for examples.

### Submit a high score
```
POST http://127.0.0.1:5000/highscore
```

* Body: `{ "username": <username>, "score": <score> }`

### Get all highscores
```
GET http://127.0.0.1:5000/highscore?start=0&count=10
```
 * Optionally get from `start` to `count` highscores

### Get a user's highscore
```
GET http://127.0.0.1:5000/highscore/<username>
```