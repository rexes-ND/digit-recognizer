# Digit Recognizer

The project is based on [Kaggle Competition: Digit Recognizer](https://www.kaggle.com/competitions/digit-recognizer).

## Frontend

### Tech Stack:
- Programming Language: `TypeScript`
- Framework: `React`
    - Third-party libraries used: 
        - `react-konva`: For drawing digit
- Styling: `TailwindCSS`

## Backend

### Tech Stack:
- Programming Language: `Python`
- Framework: `Django`
    - Third-part libraries used:
        - `celery`: For async classification task
        - `channels`: For websocket endpoint to give real-time update on `Celery` task
- Dependency:
    - `Celery` Workers
    - `redis`: For `Celery` broker and `Channel Layer` for websocket support

## Local Development

```bash
$ git clone https://github.com/rexes-ND/digit-recognizer 
$ cd digit-recognizer
$ docker compose up --build

# Now you can access http://localhost:5173/ via browser
```
