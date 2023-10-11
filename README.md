# quiz_questions_app
Simple dockerized RESTful app with FastAPI framework
### Requirements:

1. docker-compose v2.22.0 (https://github.com/docker/compose/releases)
 
### RUN
1. Clone project
```bash
$ git clone git@github.com:RBstyle/quiz_questions_app.git
$ cd quiz_questions_app/
```
2. Rename "env" file
```bash
$ mv example.env .env
```
3. Run project
```bash
$ docker-compose up
```
App running on http://0.0.0.0:8000