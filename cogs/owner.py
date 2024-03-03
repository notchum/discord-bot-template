import disnake
from disnake.ext import commands
from loguru import logger

from bot import MyBot
from helpers import SuccessEmbed


class Owner(commands.Cog):
    """An example command class for slash commands only accessible by the
    bot owner.

    This class uses disnake's subcommands.
    https://docs.disnake.dev/en/latest/ext/commands/slash_commands.html#subcommands-and-groups

    If the bot is ever scaled to many guilds, then it would be a good idea
    to use `guild_ids` in the slash command decorator to specify that these
    commands should only be registered to specific guilds.
    """

    def __init__(self, bot: commands.Bot):
        self.bot: MyBot = bot

    @commands.is_owner()
    @commands.slash_command()
    async def owner(self, inter: disnake.ApplicationCommandInteraction):
        """Top-level command group for owner commands."""
        pass

    @owner.sub_command()
    async def set_status(
        self,
        inter: disnake.ApplicationCommandInteraction,
        type: disnake.ActivityType,
        status: str,
    ):
        """Set the bot's presence/status.

        Parameters
        ----------
        type: :class:`disnake.ActivityType`
            The type of activity for the status.
        status: :class:`str`
            The status to set.
        """
        await self.bot.change_presence(
            activity=disnake.Activity(type=type, name=status)
        )
        logger.info(f"Changing status to '{status}'")
        await inter.response.send_message(
            embed=SuccessEmbed(f"Changed status to\n> {type.name} {status}")
        )

    @owner.sub_command()
    async def download_log(self, inter: disnake.ApplicationCommandInteraction):
        """Download the current log file."""
        return await inter.response.send_message(
            file=disnake.File("log/my-bot.log"), ephemeral=True
        )


def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))
