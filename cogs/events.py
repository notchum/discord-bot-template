import disnake
from disnake import commands
from loguru import logger

import models
from bot import MyBot
from helpers import utilities as utils

class Events(commands.Cog):
    """An example cog to listen/handle Discord events.
       
       This class uses disnake's event listeners.
       https://docs.disnake.dev/en/latest/api/events.html

       Two events (guild joins & updates) have actions taken
       within their respective listeners to update the 'guilds'
       collection within the MongoDB database.
    """
    def __init__(self, bot: commands.Bot):
        self.bot: MyBot = bot

    @commands.Cog.listener()
    async def on_slash_command(self, inter: disnake.ApplicationCommandInteraction):
        """ Client event when a command is used. """
        logger.info(f"{inter.guild.name}[{inter.guild.id}] | "
                    f"{inter.channel.name}[{inter.channel.id}] | "
                    f"{inter.author}[{inter.author.id}] | "
                    f"Invoked {inter.application_command.cog_name}::{inter.application_command.name}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        """ Client event when it creates or joins a guild. """
        logger.info(f"Joined {guild.name}[{guild.id}]")
        
        # Check if this guild already has a database entry
        guild_docs = await models.Guild.find_all().to_list()
        existing_guild_ids = [guild_doc.guild_id for guild_doc in guild_docs]
        if guild.id in existing_guild_ids:
            return
        
        # If the guild doesn't have a database entry, create one
        await models.Guild.insert_one(
            models.Guild(
                guild_id=guild.id,
                name=guild.name,
                bot_log_channel_id=guild.system_channel.id
            )
        )
        logger.info(f"Created database entries for guild {guild.name}[{guild.id}]")

        # Send a message to the guild to say hello!
        await guild.system_channel.send(
            embed=disnake.Embed(
                title="Hello!",
                #! Use utils.slash_command_mention() to get a clickable mention to
                #! the `/bind_log_channel` command once it is registered!
                description=f"I'm {self.bot.user.name} :wave:\n\n"
                             "Use `/bind_log_channel` to set up a channel for my logs!",
            )
        )

    @commands.Cog.listener()
    async def on_guild_update(
        self,
        before: disnake.Guild,
        after: disnake.Guild
    ):
        """ Client event when a guild is updated. """
        if before.name != after.name:
            await models.Guild.find_one(
                models.Guild.guild_id == after.id
            ).set({models.Guild.name: after.name})
            logger.info(f"{before.name}[{before.id}] | "
                        f"Changed guild name to {after.name}")

    @commands.Cog.listener()
    async def on_connect(self):
        """ Client event when it connects. """
        logger.success("CONNECTED TO DISCORD")

    @commands.Cog.listener()
    async def on_reconnect(self):
        """ Client event when it is reconnecting. """
        logger.info("RECONNECTING TO DISCORD")

    @commands.Cog.listener()
    async def on_disconnect(self):
        """ Client event when it disconnects. """
        logger.warning("DISCONNECTED FROM DISCORD")

def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))