import os
import shutil
import tempfile
import platform
from collections import namedtuple

import aiohttp
import disnake
from disnake.ext import commands
from loguru import logger
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

import models
from helpers import utilities as utils

VERSION = "0.0.1"

Config = namedtuple(
    "Config",
    [
        "DEBUG",
        "DISNAKE_LOGGING",
        "TEST_MODE",
        "DISCORD_BOT_TOKEN",
        "TEST_GUILD_ID",
        "DATABASE_URI",
        "NASA_KEY",
    ],
)


class MyBot(commands.InteractionBot):
    def __init__(self, *args, **kwargs):
        self.config: Config = kwargs.pop("config", None)
        self.version = VERSION
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        # Initialize temporary directory
        self.create_temp_dir()
        self.logger.debug(f"Initialized temp directory {self.temp_dir}")

        # Load cogs
        for extension in utils.get_cog_filenames():
            try:
                self.load_extension(extension)
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                self.logger.exception(
                    f"Failed to load extension {extension}!\t{exception}"
                )

        # Initialize database connection
        self.client = AsyncIOMotorClient(self.config.DATABASE_URI, io_loop=self.loop)
        db_list = await self.client.list_database_names()
        if "my-bot" not in db_list:
            db = self.client["my-bot"]
            await db.create_collection("settings")
            await db.create_collection("guilds")
        if self.config.TEST_MODE:
            await init_beanie(
                self.client["test-my-bot"],
                document_models=[models.BotSettings, models.Guild],
            )
            logger.warning("Running in test mode. Connected to test database.")
        else:
            await init_beanie(
                self.client["my-bot"],
                document_models=[models.BotSettings, models.Guild],
            )
            logger.success("Connected to database.")

        # Initialize aiohttp session
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def on_ready(self):
        # fmt: off
        self.logger.info("------")
        self.logger.info(f"{self.user.name} v{self.version}")
        self.logger.info(f"ID: {self.user.id}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(f"Disnake API version: {disnake.__version__}")
        self.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        self.logger.info("------")
        # fmt: on

    async def close(self):
        await self.session.close()
        await super().close()

    def create_temp_dir(self):
        self.temp_dir = os.path.join(tempfile.gettempdir(), "tmp-my-bot")
        if not os.path.exists(self.temp_dir):
            os.mkdir(self.temp_dir)

    def clear_temp_dir(self):
        for file in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                self.logger.error(f"Error deleting {file}: {e}")
