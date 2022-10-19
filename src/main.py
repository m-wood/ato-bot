"""ato-bot
-
My shitty discord bot

-Michael Wood
"""

import argparse
import errno
from types import ModuleType
import discord.errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "token", action="store",
        help="A valid Discord bot token",
    )

    args = parser.parse_args()

    if args.token is not None:
        
        try:
            import atobot
            run_ato_bot(args.token, atobot)


        except ImportError:
            print("Required module atobot not found")
            quit(errno.ENOENT)
        except discord.errors.LoginFailure:
            print("Token was rejected")
            quit(errno.EINVAL)
        
        
    else:
        print("Missing parameter: bot token")
        quit(errno.EINVAL)

def run_ato_bot(token: str, bot_module: ModuleType) -> None:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
            
    connection = bot_module.AtoBotClient(intents=intents)
    # connection.run(token)


if __name__ == "__main__":
    main()
    