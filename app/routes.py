__all__ = ["bp"]

from flask import Blueprint, Response, render_template, jsonify, request
from app.bot import bot

# This is a blueprint, which is used to declare routes for an app
# Without directly depending on the app instance itself
# This allows for decoupling of the routes and the application
bp = Blueprint("routes", __name__)


@bp.get("/")
def index() -> str:
    return render_template("view/home.html")


@bp.post("/recieve-message")
def recieve_message() -> Response:
    message = request.json["msg"]
    response = bot.handle(message)
    return jsonify({"msg": response})


@bp.post("/reset")
def reset() -> str:
    bot.reset()
    return "Bot Reset"
