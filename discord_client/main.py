import os

from dotenv import load_dotenv
from src.discord_bot import DiscordBot


def main():
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    bot = DiscordBot()
    bot.run(token=token)


if __name__ == "__main__":
    main()
