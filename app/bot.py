__all__ = ["bot"]

from copy import deepcopy
from random import shuffle
from dataclasses import dataclass
from typing import Optional
from app.data import get_all_holidays, get_all_responses, get_valid_holidays
from app.utils import is_positive_message


@dataclass
class Question:
    """
    This object will store a question.\n
    It also has the potential to store another question within.\n
    If a question is found to have a child question,
    the child question will be asked next.
    """
    question: str
    followup: Optional["Question"]
    impact: str | None


def all_questions() -> list[Question]:
    """
    Returns a pre-determined list of questions\n
    Which are shuffled.
    """
    questions = [
        Question(
            "Do you have a preferred continent?",
            Question(
                "What is your preferred continent?",
                None,
                "Continent"
            ),
            None
        ),
        Question(
            "Do you prefer active or lazy holidays?",
            None,
            "Category"
        ),
        Question(
            "Do you have a minimum star rating for your hotels?",
            Question(
                "What is your minimum rating?",
                None,
                "StarRating"
            ),
            None
        ),
        Question(
            "Do you have a preference for temperatures?",
            Question(
                "Do you prefer hot, cold, or mild?",
                None,
                "TempRating"
            ),
            None
        ),
        Question(
            "Do you have a preference for location?",
            Question(
                "Do you prefer the sea, city, or mountain?",
                None,
                "Location"
            ),
            None
        ),
        Question(
            "Do you have an upper price limit? (Per night)",
            Question(
                "What is your upper price limit?",
                None,
                "PricePerNight"
            ),
            None
        )
    ]
    shuffle(questions)
    return questions


class Bot:
    """
    This is the main part of the application\n
    It contains all of the logic for selecting user preferences\n
    and then returns the list of holidays that meet the users criteria.
    """
    def __init__(self) -> None:
        self.holidays = get_all_holidays()
        self.questions = all_questions()

        self.preference = {}
        # This is a dictionary of the users preference to be build up
        # Through the questions asked by the bot

        self.before_first_question = True
        self.question_index = 0  # Start on the first question
        self.current_question = self.questions[self.question_index]
        self.previous_question = self.current_question

    def generate_holidays(self) -> str:
        valid_holidays = deepcopy(self.holidays)

        for key, value in self.preference.items():
            valid_holidays = get_valid_holidays(
                valid_holidays,
                key,
                value
            )

        holiday_message = [
            "Thanks for using the Holiday Chat Bot!",
            "Here is a list of recommended holidays based on your preferences:"
        ]

        for holiday in valid_holidays:
            holiday_message.append(str(holiday))

        return "\n".join(holiday_message)

    def handle_impact(self, impact: str | None, message: str) -> None:
        if impact is None:
            return
        self.preference[impact] = message

    def next_question(self) -> None:
        self.question_index += 1
        self.previous_question = self.current_question
        self.current_question = self.questions[self.question_index]

    def update_question(self, message: str) -> str:
        if self.current_question.followup is not None and \
           is_positive_message(message, get_all_responses()["positive"]):
            self.current_question = self.current_question.followup
            return self.current_question.question

        elif self.question_index < len(self.questions) - 1:
            self.handle_impact(self.current_question.impact, message)
            self.next_question()
            return self.current_question.question

        else:
            self.handle_impact(self.current_question.impact, message)
            return self.generate_holidays()

    def respond(self, message: str) -> str:
        """Responds to the users message"""
        return self.update_question(message)

    def handle_message(self, message: str) -> str:
        if self.before_first_question:
            self.before_first_question = False
            return self.current_question.question
        else:
            return self.respond(message)

    def reset(self) -> None:
        """Resets the bot to it's original state, so it can be used again"""
        self.preference = {}
        self.before_first_question = True
        self.question_index = 0
        self.current_question = self.questions[self.question_index]
        self.previous_question = self.current_question


bot = Bot()
"""The instance of the bot object for use in the application"""
