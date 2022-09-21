__all__ = ["Bot", "bot"]

from copy import deepcopy
from app.data import get_all_holidays, get_all_responses, get_valid_holidays
from app.utils import is_positive_message
from app.question import all_questions


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
        """The preference is a dictionary of the users choices"""

        self.before_first_question = True
        self.question_index = 0
        self.current_question = self.questions[self.question_index]
        self.previous_question = self.current_question

    def _generate_holidays(self) -> str:
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

    def _handle_impact(self, impact: str | None, message: str) -> None:
        if impact is None:
            return
        self.preference[impact] = message

    def _next_question(self) -> None:
        self.question_index += 1
        self.previous_question = self.current_question
        self.current_question = self.questions[self.question_index]

    def _update_question(self, message: str) -> str:
        if self.current_question.followup is not None and \
           is_positive_message(message, get_all_responses()["positive"]):
            self.current_question = self.current_question.followup
            return self.current_question.question

        elif self.question_index < len(self.questions) - 1:
            self._handle_impact(self.current_question.impact, message)
            self._next_question()
            return self.current_question.question

        else:
            self._handle_impact(self.current_question.impact, message)
            return self._generate_holidays()

    def _respond(self, message: str) -> str:
        return self._update_question(message.lower())

    def handle(self, message: str) -> str:
        if self.before_first_question:
            self.before_first_question = False
            return self.current_question.question
        else:
            return self._respond(message)

    def reset(self) -> None:
        """Resets the bot to it's original state, so it can be used again"""
        self.preference = {}
        self.before_first_question = True
        self.question_index = 0
        self.current_question = self.questions[self.question_index]
        self.previous_question = self.current_question


bot = Bot()
"""The instance of the bot object for use in the application"""
