from app.bot import Bot
from app.question import Question
from app.holiday import Holiday

_questions: list[Question] = [
    Question("", None, "TestImpact"),
    Question("", None, "TestImpact"),
    Question("", None, "TestImpact"),
    Question("", None, "TestImpact")
]

_holidays: list[Holiday] = [
    Holiday(
        1,
        "TestHotel",
        "TestCity",
        "TestContinent",
        "TestCountry",
        "TestCategory",
        5,
        "TestTempRating",
        "TestLocation",
        50
    )
]


def setup_bot(bot: Bot) -> None:
    bot.questions = _questions
    bot.current_question = bot.questions[bot.question_index]
    bot.before_first_question = False
    bot.holidays = _holidays
    bot.username = "username"


def test_bot_sets_preferences(bot: Bot) -> None:
    setup_bot(bot)
    bot.handle("yes")
    assert bot.preference.get("TestImpact") is not None
    assert len(bot.preference.keys()) == 1


def test_bot_reset_clears_preference(bot: Bot) -> None:
    setup_bot(bot)
    bot.handle("yes")
    assert bot.preference.get("TestImpact") is not None
    assert len(bot.preference.keys()) == 1
    bot.reset()
    assert bot.preference.get("TestImpact") is None
    assert len(bot.preference.keys()) == 0


def test_bot_generates_correct_holidays(bot: Bot) -> None:
    setup_bot(bot)
    bot.preference = {
        "Continent": "TestContinent",
        "StarRating": 5,
        "Location": "TestLocation"
    }

    msg = bot._generate_holidays()

    assert "Thanks for using the Holiday Chat Bot username" in msg
    assert "Hotel TestHotel" in msg
    assert "Rating: 5⭐" in msg
    assert ", TestCountry" in msg


def test_bot_first_req_sets_usn_second_incr_question_idx(bot: Bot) -> None:
    bot.questions = [
        Question("", None, None),
        Question("", None, None),
        Question("", None, None)
    ]
    bot.current_question = bot.questions[0]

    assert bot.username == ""
    assert bot.before_first_question
    assert bot.question_index == 0
    bot.handle("Isaac")
    assert bot.username == "Isaac"
    assert not bot.before_first_question
    assert bot.question_index == 0
    bot.handle("Yes")
    assert bot.question_index != 0


def test_bot_handle_impact_returns_if_impact_is_none(bot: Bot) -> None:
    assert bot._handle_impact(None, "") is None


def test_bot_generates_holidays_with_no_questions_left(bot: Bot) -> None:
    setup_bot(bot)
    bot.handle("")
    bot.handle("")
    bot.handle("")

    assert "Thanks for using the Holiday Chat Bot username" in bot.handle("")


def test_bot_question_follow_is_set(bot: Bot) -> None:
    bot.username = "username"
    bot.before_first_question = False
    bot.questions = [Question("", Question("", None, "Continent"), None)]
    bot.current_question = bot.questions[0]
    bot.holidays = _holidays

    assert bot.handle("yes") == ""
    holiday_msg = bot.handle("TestContinent")
    assert bot.current_question == bot.questions[0].followup
    assert "Thanks for using the Holiday Chat Bot username" in holiday_msg
    assert ", TestCountry" in holiday_msg


def test_bot_first_message_sets_username(bot: Bot) -> None:
    bot.handle("Isaac")

    assert bot.username == "Isaac"


def test_bot_invalid_response_asks_question_again(bot: Bot) -> None:
    bot.before_first_question = False
    bot.questions = [
        Question("", Question("", None, "TestImpact"), None)
    ]
    bot.current_question = bot.questions[0]

    response = bot.handle("abcdef")

    assert "I'm sorry, I didn't understand 'abcdef'" in response
    assert "abcdef" in response
    assert "The question was: " in response
