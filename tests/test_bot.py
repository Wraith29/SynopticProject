from app.bot import Bot, Question


_dummy_questions = [
    Question("reply with yes", None, "test")
]


def test_bot_updates_preference(bot: Bot) -> None:
    bot.questions = _dummy_questions
    bot.current_question = bot.questions[bot.question_index]

    bot.handle_message("yes")

    print(bot.preference)

    assert len(bot.preference.keys())
    assert bot.preference.get("test") is not None
