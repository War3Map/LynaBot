import csv
from pprint import pprint

from additional.field_of_dreams.game_config import DEFAULT_QUESTIONS_FILE


class LoadQuestionsError(Exception):
    def __init__(self, message="LoadQuestionsError: can't load questions!", ex=None):
        self.message = message
        self.ex = ex
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} {self.ex}'


def load_from_file(question_file):
    questions_dict = {}
    with open(question_file, "r", encoding="utf-8") as question:
        reader = csv.reader(question, delimiter=";")
        for line in reader:
            if len(line) >= 2:
                word = line[1].upper()
                question = line[0]
                questions_dict[word] = question
    return questions_dict


def try_load_questions(questions_file):
    try:
        questions = load_from_file(questions_file)
        return questions
    except (FileExistsError,
            FileNotFoundError,
            PermissionError,
            ValueError,
            UnicodeDecodeError) as ex:
        raise LoadQuestionsError(ex=ex)


def load_questions(question_file):
    """
    Loads questions from csv file
    :return:
    """

    if question_file is None:
        questions = try_load_questions(DEFAULT_QUESTIONS_FILE)

    else:
        questions = try_load_questions(question_file)
    return questions




