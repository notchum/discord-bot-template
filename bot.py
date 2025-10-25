import os
import shutil
import tempfile
import platform
import tomllib
from collections import namedtuple

import aiohttp
import disnake
from disnake.ext import commands
from loguru import logger
from beanie import init_beanie
from pymongo import AsyncMongoClient

import models
import utils


Config = namedtuple(
    "Config",
    [
        "DEBUG",
        "DISNAKE_LOGGING",
        "TEST_MODE",
        "DISCORD_BOT_TOKEN",
        "TEST_GUILDS",
        "DATABASE_URI",
        "NASA_KEY",
    ],
)


class MyBot(commands.InteractionBot):
    def __init__(self, *args, **kwargs):
        self.config: Config = kwargs.pop("config", None)
        self.version = self.get_version()
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        # Initialize temporary directory
        self.create_temp_dir()
        logger.debug(f"Initialized temp directory {self.temp_dir}")

        # Load cogs
        for extension in utils.get_cog_names():
            try:
                self.load_extension(extension)
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                logger.exception(f"Failed to load extension {extension}!\t{exception}")

        # Initialize database connection
        self.client = AsyncMongoClient(self.config.DATABASE_URI)
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

        # Create the global bot settings entry if it doesn't exist
        await self.create_settings_entry()

        # Initialize aiohttp session
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def on_ready(self):
        # fmt: off
        logger.info("------")
        logger.info(f"{self.user.name} v{self.version}")
        logger.info(f"ID: {self.user.id}")
        logger.info(f"Python version: {platform.python_version()}")
        logger.info(f"Disnake API version: {disnake.__version__}")
        logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        logger.info("------")
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
                logger.error(f"Error deleting {file}: {e}")

    def get_version(self, pyproject_path: str = "pyproject.toml") -> str:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
            return data.get("project", {}).get("version")

    async def create_settings_entry(self):
        settings_doc = await models.BotSettings.find_all().to_list()
        if len(settings_doc) == 0:
            settings_doc = await models.BotSettings.insert_one(
                models.BotSettings(toggle=False)
            )
            logger.success(f"Created settings entry for my-bot [{settings_doc.id}]")
