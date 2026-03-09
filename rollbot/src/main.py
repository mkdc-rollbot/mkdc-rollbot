from discord_bot import DiscordBot


def main():
    with open("../token.txt", "r") as f:
        token = f.readlines()[0]
    bot = DiscordBot()
    bot.run(token=token)


if __name__ == "__main__":
    main()
