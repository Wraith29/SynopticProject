__all__ = ["Question"]

from random import shuffle
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Question:
    """
    This object represents a question for the user.

    :question: str - The question which will be sent to the User.\n
    :followup: Optional[Question] - The followup question to be sent
    to the user or None.\n
    :impact: str - The holiday preference which will be impacted
    by this question.
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
            "Do you prefer active or lazy holidays? or either",
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
