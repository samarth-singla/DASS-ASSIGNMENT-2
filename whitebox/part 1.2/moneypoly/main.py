"""Entry point for running an interactive MoneyPoly session."""

from moneypoly.game import Game


def get_player_names():
    """Read comma-separated names and return a normalized player list."""
    print("Enter player names separated by commas (minimum 2 players):")
    raw = input("> ").strip()
    names = [n.strip() for n in raw.split(",") if n.strip()]
    return names


def main():
    """Create and execute a game using user-provided player names."""
    names = get_player_names()
    try:
        game = Game(names)
        game.run()
    except KeyboardInterrupt:
        print("\n\n  Game interrupted. Goodbye!")
    except ValueError as exc:
        print(f"Setup error: {exc}")


if __name__ == "__main__":
    main()
