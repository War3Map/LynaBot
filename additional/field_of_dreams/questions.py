import csv
from pprint import pprint

QUESTIONS_FILE = "questions.csv"


def load_questions(question_file):
    """
    Loads questions from csv file
    :return:
    """
    questions_dict = {}
    with open(question_file, "r", encoding="utf-8") as question:
        reader = csv.reader(question, delimiter=";")
        for line in reader:
            if len(line) >= 2:
                word = line[1].upper()
                question = line[0]
                questions_dict[word] = question
    return questions_dict

