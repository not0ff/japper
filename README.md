# Japper
Japper is a minimal micro-blogging web app that with it's social features allows users to connect together and share their thoughts with the world. By being built in Flask web framework and with user interface designed using Bootstrap toolkit it delivers fast and good-looking fronted website.

## Table of Contents
- [Japper](#japper)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Features](#features)
  - [Technologies](#technologies)

## Installation
1. Create a virtual python environment
    ```
    $ python -m venv venv
    ```
2. Activate it
- On Windows:
  ```
  $ .\venv\Scripts\activate.bat
  ```
- On Linux:
  ```
  $ source venv/bin/activate
  ```
3. Install required dependencies
   ```
   $ pip install -r requirements.txt
   ```

## Usage
Quick guide how to run the project

1. Create .env file with flask secret key to sign and encrypt cookies
   ```
   SECRET_KEY = [secure_key_here]
   ```

2. Navigate to source directory
   ```
   $ cd src/
   ```
3. Initialize local testing database with flask-migrate
   ```
   $ flask db init
   $ flask db migrate
   $ flask db upgrade
   ```
4. Start a local development server
   ```
   $ flask run
   ```
5. Visit http://127.0.0.1:5000 on your browser

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