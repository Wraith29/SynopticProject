"""
This is the entry point of my application.
"""

from app import create_app


def main() -> None:
    app = create_app()
    app.run(port=5000)


if __name__ == "__main__":
    main()
