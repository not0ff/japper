# Japper
Japper is a minimal micro-blogging web app that with it's social features allows users to connect together and share their thoughts with the world. By being built in Flask web framework and with user interface designed using Bootstrap toolkit it delivers fast and good-looking fronted website.

## Table of Contents
- [Japper](#japper)
  - [Table of Contents](#table-of-contents)
  - [Running locally](#running-locally)
  - [Running with docker](#running-with-docker)
  - [Features](#features)
  - [Technologies](#technologies)

## Running locally
1. Make sure you have uv installed
   ```
   $ pip install uv
   ```
2. Install project's dependencies
   ```
   $ uv sync
   ```
3. Activate the created virtual environment
   - On Windows:
   ```
   $ .\.venv\Scripts\activate.bat
   ```
   - On Linux:
   ```
   $ source .venv/bin/activate
   ```
4. Set env variable with flask secret key
   - On Windows:
      ```
      $ set SECRET_KEY=<secure_key_here>
      ```
   - On Linux:
      ```
      $ export SECRET_KEY=<secure_key_here>
      ```
5. Navigate to source directory
   ```
   $ cd src/
   ```
6. Initialize local sqlite database with flask-migrate
   ```
   $ flask db upgrade
   ```
7. Start a development server
   ```
   $ gunicorn --bind 0.0.0.0:8000 wsgi:app
   ```
8. Visit http://127.0.0.1:8000 on your browser

## Running with docker
1. Create .env file or set flask secret key and postgres credentials manually (required variables in .env.example file)
2. Run docker compose
```
$ docker compose up --build -d
```
3. Go to http://127.0.0.1:8000
4. Then later
```
$ docker compose down
```

## Features
List of most important features include:
- **Posting** about what interests you
- **Liking** other people's messages
- **Following** users you like
- Getting relevant **notifications**
- **Searching** for interesting content

## Technologies
Japper was built with following frameworks and tools:
- <ins>Flask</ins> -> Main web framework
- <ins>SqlAlchemy</ins> -> SQL database querying
- <ins>Bootstrap</ins> -> Frontend components and styling
- <ins>Javascript</ins> -> For making site more interactive

It also uses flask extensions such as flask-login, flask-migrate, flask-moment, flask-reuploaded, flask-sqlalchemy and flask-wtf to make the website more robust and reliable.
