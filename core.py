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
    while(True):
        print("What's the right answer?")
        print(f"[?] Question: {question}")
        for i in range(4):
            print(f"[? | {i + 1}] {get_answer_texts(driver)[i]}")
        while (True):
            try:
                print("[? | [1-4]] -> ", end="")
                new_answer = int(input())
                break
            except:
                pass
        print("[?] Is this correct?")
        print("[?] Question:", question)
        print("[?] Answer:", get_answer_texts(driver)[new_answer - 1])
        print("[? | yN] -> ", end="")
        if input().lower() == "y":
            answers[question] = get_answer_texts(driver)[new_answer - 1]
            save_answer_csv(answers)
            break # accept input

def select_correct_answer(driver, answers, question, answer_text):
    solved = False
    for answer_object in get_answer_objects(driver):
        if answer_object.find_element_by_xpath("./span[2]").text.lower() == answer_text.lower():
            print(f"[i] Q: {question} :: A: {answer_text}")
            solved = True
            answer_object.find_element_by_xpath("./span[1]/a").click()
    
    if not solved:
        print("FATAL: This question doesn't have a valid answer.")
        print("FATAL: Repair the issue and try again")
        print("FATAL: I'm too lazy to handle this nicely and it's midnight")
        exit(1)

def get_correct_answer(driver, question, answers):
    if question not in answers:
        print("ERR: Found a question without a known answer.")
        get_missing_answer(driver, question, answers)
    return answers[question]

def solve_question(driver, answers):
    counter = 20
    sleep(5)
    while(len(get_answer_texts(driver)[3]) < 1 and counter > 0):
        sleep(2)
        counter -= 1
        print(f"Waiting... [{counter}] [{ get_answer_texts(driver) }]")
    
    question = get_question_text(driver)
    correct_answer_text = get_correct_answer(driver, question, answers)
    select_correct_answer(driver, answers, question, correct_answer_text)

    # NEXT!
    driver.find_element_by_id("nextQuestion").click()
    print(f"[i] Advancing to next question")

    
    
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
            answers[answer[0]] = answer[1]
        return answers
    return None

def main():
    answers = load_question_database()
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    #driver.get("https://www.freekigames.com/")

    quizzes = [
        "tenth-grade-vocabulary-trivia",
        "baseball-trivia",
        "advanced-spelling-trivia",
        "ninth-grade-vocabulary-trivia",
        "landforms-trivia",
        "solar-system-trivia",
        "famous-world-leaders",

    ]

    print("Which quiz?")
    for i in range(len(quizzes)):
        print(f"[? | {i + 1}] {quizzes[i]}")
    print(f"[? | 1-{len(quizzes)}] -> ", end="")

    driver.get("https://www.freekigames.com/" + quizzes[int(input())-1])

    for i in range(20):
        print(f"Solving {i}")
        solve_question(driver, answers)

    input("Press enter when done with this quiz. The window will close.")
    driver.quit()




    # driver.find_element_by_xpath("/html/body/div[4]/div/div[3]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div/div[1]/div[1]/span/a").click()
    # driver.switch_to.frame(driver.find_element_by_id("jPopFrame_content"))
    # sleep(1)
    # driver.find_element_by_xpath("//*[@id=\"userName\"]").send_keys(config.USERNAME)
    # sleep(1.2)
    # driver.find_element_by_xpath("//*[@id=\"password\"]").send_keys(config.PASSWORD)
    # sleep(0.5)
    # driver.find_element_by_xpath("//*[@id=\"bp_login\"]").click()
    # print()


if __name__ == '__main__':
    main()