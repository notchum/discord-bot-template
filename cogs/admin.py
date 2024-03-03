import disnake
from disnake.ext import commands
from loguru import logger

import models
from bot import MyBot
from helpers import SuccessEmbed

class Admin(commands.Cog):
    """An example command class for slash commands only accessible by a
       guild's administrator(s).
       
       This class uses an ODM (Beanie) to interact with a MongoDB collection.
    """
    def __init__(self, bot: commands.Bot):
        self.bot: MyBot = bot

    @commands.slash_command(default_member_permissions=disnake.Permissions(administrator=True))
    async def bind_log_channel(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ):
        """Bind the channel for bot logs in this guild."""
        await inter.response.defer()

        # Find the database entry for this guild
        guild_doc = await models.Guild.find_one(
            models.Guild.bot_log_channel_id == inter.guild.id
        )
        
        # Set the ID
        guild_doc.bot_log_channel_id = channel.id

        # Commit changes to the database
        await guild_doc.save()

        # Log it and send a message in Discord as well
        logger.info(f"{inter.author.name}[{inter.author.id}] binded {channel.name}[{channel.id}] for logging.")
        await inter.edit_original_response(embed=SuccessEmbed(f"Binded {channel.mention} for logging."))

def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))