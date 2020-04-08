# QuizSolver
Uses selenium to automatically answer trivia questions on a certain site for game rewards.

This does not solve the captchas for obvious reasons. It leaves that to you.

## Install
Dependencies:
- pipenv
- python 3.7+
- firefox gecko driver for selenium (will add others soon)

Set up:
- `pipenv install`
- Ensure you have entered the credentials into the config python file. This repo has a file named `config_EXAMPLE.py`. Remove `_EXAMPLE` so this file reads `config.py` before using. Otherwise, config.py is missing or something like that will be an error.

## Run
`pipenv run python core.py`

You'll be prompted for the quizzes to solve. enter one number, or several seperated by commas like so. `1,2,3,4,5`. Note there's no spaces.

If a question isn't recognized, you'll be prompted to enter the right answer in the terminal window. Enter it there, as it will remember the right answer for the next time.

In the event a saved answer isn't in the choices, the program will ask you to hit the checkbox of the right answer. Without clicking Next, choose the right answer, and hit ENTER in the terminal so the answer can be fixed.



## Profit. No, really.
