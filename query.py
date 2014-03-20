__author__ = 'Steven'

import re


class Question:
    def __init__(self, question, answers):
        self._answered = False
        self._question = question
        self._answers = answers
        self._resp = None
        self._key = None

    def message(self):
        return self._question

    def answer(self, reconstructed):
        for answer, action in self._answers:
            if answer in reconstructed or re.match(answer, reconstructed):
                self._key = answer
                self._resp = reconstructed
                self._answered = True
                return action(reconstructed)
        return "Your answer does not match with any expected response. Please try again."

    def answered(self):
        return self._answered