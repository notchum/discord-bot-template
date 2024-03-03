import os
import asyncio

import disnake
from loguru import logger
from dotenv import load_dotenv

from bot import MyBot, Config

async def main():
    # Load the environment variables
    load_dotenv()

    # Create config
    config = Config(
        DEBUG=os.environ["DEBUG"] in ("1", "True", "true"),
        DISNAKE_LOGGING=os.environ["DISNAKE_LOGGING"] in ("1", "True", "true"),
        TEST_MODE=os.environ["TEST_MODE"] in ("1", "True", "true"),
        DISCORD_BOT_TOKEN=os.environ["DISCORD_BOT_TOKEN"],
        TEST_GUILD_ID=os.environ["TEST_GUILD_ID"],
        DATABASE_URI=os.environ["DATABASE_URI"],
        NASA_KEY=os.environ["NASA_KEY"],
    )

    # Create logging file
    logger.add(
        "log/my-bot.log",
        level="DEBUG" if config.DEBUG else "INFO",
        rotation="12:00"
    )
    if config.DISNAKE_LOGGING:
        pass # TODO

    # Create intents
    intents = disnake.Intents.default()
    intents.members = True
    intents.message_content = True
    
    # Create bot
    bot = MyBot(
        config=config,
        test_guilds=[config.TEST_GUILD_ID],
        intents=intents,
    )
    await bot.setup_hook()
    await bot.start(config.DISCORD_BOT_TOKEN)

asyncio.run(main())