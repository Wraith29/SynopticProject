__all__ = ["bot"]

from random import shuffle
from dataclasses import dataclass
from typing import Optional
from app.data import get_all_holidays, get_all_responses
from app.holiday import Holiday
from app.utils import sanitise


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
                "Contintent"
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
                "Do you prefer, hot, cold, or mild?",
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
            "Do you have an upper price limit?",
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
    def __init__(self) -> None:
        self.holidays = get_all_holidays()
        self.responses = get_all_responses()
        self.questions = all_questions()

        self.preference = {}
        # This is a dictionary of the users preference to be build up
        # Through the questions asked by the bot

        self.before_first_question = True
        self.question_index = 0  # Start on the first question
        self.current_question = self.questions[self.question_index]
        self.previous_question = self.current_question

    def generate_holidays(self) -> str:
        valid_holidays: list[Holiday] = []
        # TODO: Make This work!!!!
        for holiday in self.holidays:
            for key, value in self.preference.items():
                if getattr(holiday, str(key)).lower() == value.lower():
                    valid_holidays.append(holiday)

        print(valid_holidays)

        return "Thanks for using the Holiday bot!"

    def handle_impact(self, impact: str, message: str) -> None:
        self.preference[impact] = message

    def respond(self, message: str) -> str:
        """Responds to the users message"""
        if self.before_first_question:
            self.before_first_question = False
            return self.current_question.question

        if self.current_question.followup is not None and \
           sanitise(message) in self.responses["positive"]:
            self.current_question = self.current_question.followup
        elif self.question_index < len(self.questions) - 1:
            self.handle_impact(self.current_question.impact, message)
            self.question_index += 1
            self.previous_question = self.current_question
            self.current_question = self.questions[self.question_index]
        else:
            self.handle_impact(self.current_question.impact, message)
            return self.generate_holidays()

        return self.current_question.question

    def handle_message(self, message: str) -> str:
        msg_to_send = self.respond(message)

        return msg_to_send

    def reset(self) -> None:
        """Resets the bot to it's original state, so it can be used again"""
        self.preference = {}
        self.before_first_question = True
        self.question_index = 0
        self.current_question = self.questions[self.question_index]
        self.previous_question = self.current_question


bot = Bot()
