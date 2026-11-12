import random
import os
os.environ["FORCE_COLOR"] = "1"
from termcolor import cprint

QUESTION = "question"
ANSWERS = "answers"
CORRECT = "correct"

def ask_question(index, item, options):
    print(f"[{index}] {item}")
    for answer in options:
        print(f"[{answer:<12}]")

    return input("Enter the correct answer? ").upper().strip()
def run_quiz(quiz):
    random.shuffle(quiz)
    score = 0
    for index, item in enumerate(quiz, 1):
        answer = ask_question(index, item[QUESTION], item[ANSWERS])
        if answer == item[CORRECT]:
            cprint("Correct answer!", "green")
            score += 1
        else:
            cprint(f"The answer is incorrect,and the correct answer is {item[CORRECT]}!", "red")
    print(f"You answered {len(quiz)} out of {score} question correctly. ")

def main():
    item = [
        {
            QUESTION: 'what is the capital of Iran?',
            ANSWERS: ['A. Isfahan', 'B. Shiraz', 'C. Tehran', 'D. Bushehr'],
            CORRECT: "C"
        },
        {
            QUESTION: 'Which planet is closest to Earth?',
            ANSWERS: ['A. Mars', 'B. Venus', 'C. Earth', 'D. Jupiter'],
            CORRECT: "A"
        },
        {
            QUESTION: 'Wha is 7 * 8?',
            ANSWERS: ['A. 35', 'B. 12', 'C. 65', 'D. 56'],
            CORRECT: "D"
        },
        {
            QUESTION: 'What is the largest ocean in thd world?',
            ANSWERS: ['A. Atlantic', 'B. Pacific', 'C. Indian', 'D. Arctic'],
            CORRECT: "B"
        }
    ]
    run_quiz(item)

if __name__ == "__main__":
    main()