import disnake
from disnake.ext import commands
from loguru import logger

import models
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
    Furthermore, to only allow certain users to even access the 'owner' slash
    commands group, go to the server(s) in which the commands are registered,
    then go to:
        - Server Settings > Integrations > Bots and Apps >
        {Name of your bot} Manage > Commands > /owner
        - Click 'Add roles or members' and select the '@everyone' role
        - Select the red 'X' for the '@everyone' override
        - Click 'Add roles or members' and add yourself
        - Select the green check for yourself
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
            embed=SuccessEmbed(
                f"Changed status to\n> {disnake.ActivityType(type).name} {status}"
            )
        )

    @owner.sub_command()
    async def settings_toggle(self, inter: disnake.ApplicationCommandInteraction):
        """Toggles the 'toggle' field in the settings.

        This is an example of how you can write
        commands to change any settings that you
        want to apply across all guilds that your
        bot is a member in (global settings).
        """
        # There is only one entry in the settings collection, since
        # these settings are global and not per-guild
        settings_doc = await models.BotSettings.find_all().to_list()
        settings_doc = settings_doc[0]

        # Simply toggle the boolean
        settings_doc.toggle = not settings_doc.toggle

        # Save the settings to the database
        settings_doc.save()

        # Send a message with the new settings
        await inter.response.send_message(
            content=f"Toggled settings.toggle to `{settings_doc.toggle}`!"
        )

    @owner.sub_command()
    async def download_log(self, inter: disnake.ApplicationCommandInteraction):
        """Download the current log file."""
        return await inter.response.send_message(
            file=disnake.File("logs/my-bot.log"), ephemeral=True
        )


def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))
