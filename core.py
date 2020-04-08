import csv
from time import sleep
from xmlrpc.client import boolean

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import config
from selenium.webdriver.support import wait



def save_answer_csv(answers):
    w = csv.writer(open("answers.csv", "w"))
    for key, val in answers.items():
        w.writerow([key, val])

def get_missing_answer(driver, question, answers):
    print("[?] What's the right answer?")
    print(f"[?] Question: {question}")
    for i in range(4):
        print(f"[? | {i + 1}] {get_answer_texts(driver)[i]}")
    while (True):
        try:
            print("[? | [1-4]] -> ", end="")
            new_answer = int(input())
            answers[question] = get_answer_texts(driver)[new_answer - 1]
            save_answer_csv(answers)
            break
        except:
            pass

def select_correct_answer(driver, answers, question, answer_text):
    solved = False
    for answer_object in get_answer_objects(driver):
        if answer_object.find_element_by_xpath("./span[2]").text.lower() == answer_text.lower():
            print(f"[i] Q: {question} :: A: {answer_text}")
            solved = True
            answer_object.find_element_by_xpath("./span[1]/a").click()

    if not solved:
        print("[!] FATAL: This question is known yet doesn't have a valid answer.")
        print("[!] FATAL: Repair the issue and try again")
        print("[!] FATAL: I'm too lazy to handle this nicely and it's midnight")
        print("[!] Press enter when you've selected the right answer.")
        print("[!] Do not press 'Next Question'. It will cause issues.")
        print("[!] ->...", end="")
        input()


def get_correct_answer(driver, question, answers):
    if question not in answers:
        print("[?] Found a question without a known answer.")
        get_missing_answer(driver, question, answers)
    return answers[question]

def solve_question(driver, answers):
    counter = 20
    sleep(5)
    while(len(get_answer_texts(driver)[3]) < 1 and counter > 0):
        sleep(2)
        counter -= 1
        print(f"Waiting...(Is the browser hidden?) [{counter}] [{ get_answer_texts(driver) }]")

    question = get_question_text(driver)
    correct_answer_text = get_correct_answer(driver, question, answers)
    select_correct_answer(driver, answers, question, correct_answer_text)

    # NEXT!
    driver.find_element_by_id("nextQuestion").click()
    # print(f"[d] Advancing to next question")



def get_question_text(driver):
    return driver.find_element_by_css_selector(".quizQuestion").text

def get_answer_objects(driver):
    return driver.find_elements_by_css_selector(".answer")

def get_answer_texts(driver) -> []:
    question_texts = []
    questions = get_answer_objects(driver)
    for i in range(4):
        question_texts.append(questions[i].find_element_by_xpath("./span[2]").text)
    return question_texts

def load_question_database():
    with open("answers.csv", newline="") as csv_file:
        answers_file = csv.reader(csv_file)
        answers = {}
        for answer in answers_file:
            try:
                answers[answer[0]] = answer[1]
            except IndexError:
                print(f"Bad CSV entry: `{answer}`")
        return answers
    return None

def open_login_window(driver):
    finished_medallion = driver.find_element_by_css_selector(
        ".quizMedallion > div:nth-child(2) > a:nth-child(1)").click()
    driver.switch_to.frame(driver.find_element_by_id("jPopFrame_content"))
    driver.implicitly_wait(3)
    try:
        driver.find_element_by_css_selector("#userName").send_keys(config.USERNAME)
        driver.find_element_by_css_selector("#password").send_keys(config.PASSWORD)
    except:
        print("[i] Seems you're already logged in. I'll skip that part.")
    driver.implicitly_wait(10)

def main():
    answers = load_question_database()
    quizzes = [
        "tenth-grade-vocabulary-trivia",
        "baseball-trivia",
        "ninth-grade-vocabulary-trivia",
        "landforms-trivia",
        "solar-system-trivia",
        "famous-world-leaders",
        "weather-trivia",
        "habitats-trivia",
        "eleventh-grade-vocabulary-trivia",
        "american-presidents-trivia",
        "big-cats-trivia",
        "heart-trivia",
        "state-animals-trivia",
    ]

    print("Which quiz? (or many by using commas)")
    for i in range(len(quizzes)):
        print(f"[? | {i + 1}] {quizzes[i]}")

    print(f"[? | 1-{len(quizzes)}] -> ", end="")
    selected_quizzes = list(map(lambda x: int(x), input().split(",")))
    driver = webdriver.Firefox()
    driver.set_window_position(0, 0)
    driver.set_window_size(600, 600)
    driver.implicitly_wait(10)
    for quiz in selected_quizzes:
        driver.get("https://www.freekigames.com/" + quizzes[quiz])

        try:
            for i in range(12):
                # print(f"[d] Solving {i}")
                solve_question(driver, answers)
        except:
            print("[!] Crashed. The quiz might be done.")

        open_login_window(driver)
        print("[i] All done! Press enter when you're done with the window.")
        input("[?] -> ...")
        driver.switch_to.default_content()

    driver.quit()


if __name__ == '__main__':
    main()
