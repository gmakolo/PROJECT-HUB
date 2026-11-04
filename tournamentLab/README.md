# TournamentLab

TournamentLab is a simple football tournament management system built with Python.

I built this project to practise Python and learn how to organise a project into different files. It allows users to create a tournament, register teams, record match results and view league standings.

## Features

- Create a tournament with 4 or 8 teams.
- Register teams and prevent duplicate names.
- Automatically generate fixtures.
- Record match results.
- View all teams and fixtures.
- View the league table.
- View statistics for each team.
- View tournament awards.
- Save tournament data to a JSON file.
- Load saved tournament data.
- Check results using automated tests.

## How to Run

Make sure Python 3 is installed on your computer.

1. Open the TournamentLab folder in your terminal.
2. Run this command:

```bash
python3 main.py
```

3. Follow the instructions displayed on the screen.

## How to Run the Tests

To check that the project is working correctly, run:

```bash
python3 -m unittest discover -s test -v
```

## Project Structure

```text
TournamentLab/
│
├── main.py
├── cli.py
├── teams.py
├── fixtures.py
├── results.py
├── standings.py
├── storage.py
│
├── test/
│   ├── test_engineer_a.py
│   ├── test_engineer_b.py
│   └── test_storage.py
│
└── tournament.json
```

## Technologies Used

- Python 3
- JSON
- Unittest

## What I Learned

While working on this project, I practised:

- Writing and using Python functions.
- Working with lists and dictionaries.
- Splitting a project into different files.
- Handling errors and invalid inputs.
- Working with JSON files.
- Writing and running automated tests.
- Using Git and GitHub to manage my project.

## Author
makolo Gift

Built as a Python learning project.