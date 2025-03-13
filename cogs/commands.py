import os
import json

import aiofiles
import disnake
from disnake.ext import commands
from loguru import logger

from bot import MyBot
from helpers import ErrorEmbed
from views import Paginator


class Commands(commands.Cog):
    """An example command class for slash commands.

    This class creates a basic slash command.
    https://docs.disnake.dev/en/latest/ext/commands/slash_commands.html#basic-slash-command

    This class shows how to perform API requests with aiohttp (with error handling).

    This class shows how to download files to the bot's temporary directory with aiofiles.
    Refer to tasks.py to see how the temporary directory is periodically cleaned.
    """

    def __init__(self, bot: MyBot):
        self.bot = bot

    @commands.slash_command()
    async def download_file(
        self, inter: disnake.ApplicationCommandInteraction, url: str
    ):
        """Download an file from a URL.

        Parameters
        ----------
        url: :class:`str`
            The URL to the image to download.
        """
        await inter.response.defer()

        # Extract the filename from the URL
        filename = os.path.basename(url).split("?")[0]

        # Create the file system path to save the file at
        # Note the use of self.bot.temp_dir to save the
        # file in a temporary location.
        filepath = os.path.join(self.bot.temp_dir, filename)

        # Check if the file already exists; download it if not
        if os.path.exists(filepath):
            logger.info(f"File at {url} already exists at {filepath}")
        else:
            try:
                # GET request using the aiohttp session
                async with self.bot.session.get(url) as response:
                    if response.status != 200:
                        return await inter.edit_original_response(
                            embed=ErrorEmbed(
                                f"Downloading media {url} returned status code `{response.status}`"
                            )
                        )

                    # Write the returned data to the file system
                    async with aiofiles.open(filepath, mode="wb") as f:
                        await f.write(await response.read())
                    logger.info(f"Downloaded file at {url} to {filepath}")
            except Exception as err:
                return await inter.edit_original_response(
                    embed=ErrorEmbed(f"Downloading media returned invalid data! {err}")
                )

        # Create a file object that can be uploaded to Discord
        file = disnake.File(filepath)

        # Finally, send the file to Discord
        await inter.edit_original_response(file=file)

    @commands.slash_command()
    async def earth(self, inter: disnake.ApplicationCommandInteraction):
        """Get images of earth via NASA's EPIC camera on the NOAA DSCOVR."""
        await inter.response.defer()

        # GET request using the aiohttp session
        try:
            async with self.bot.session.get(
                url=f"https://epic.gsfc.nasa.gov/api/natural?api_key={self.nasa_key}"
            ) as response:
                if response.status != 200:
                    return await inter.edit_original_response(
                        embed=ErrorEmbed(
                            f"NASA API returned status code `{response.status}`"
                        )
                    )
                body = await response.json()
                data = json.dumps(body)
                output = json.loads(data)
        except Exception as err:
            return await inter.edit_original_response(
                embed=ErrorEmbed(
                    f"NASA API returned invalid data! It might be broken right now - try again later.\n```\n{err}```"
                )
            )

        # Create a list of embeds with the data returned
        embeds = []
        for img_info in output[::2]:
            img_lbl = img_info["image"]
            img_date = img_info["date"]
            img_id = img_info["identifier"]
            img_cap = img_info["caption"]
            img_lat = img_info["coords"]["centroid_coordinates"]["lat"]
            img_lon = img_info["coords"]["centroid_coordinates"]["lon"]
            img_url = f"https://epic.gsfc.nasa.gov/archive/natural/{img_id[:4]}/{img_id[4:6]}/{img_id[6:8]}/png/{img_lbl}.png"
            embed = disnake.Embed(
                color=disnake.Color.dark_purple(),
                title=img_cap,
                description=f"Date: {img_date}\nLatitude: {img_lat}\nLongitude: {img_lon}",
            )
            embed.set_image(url=img_url)
            embeds.append(embed)

        # Create a paginator and add the view to the message
        page_view = Paginator(embeds, inter.author)
        message = await inter.edit_original_response(embed=embeds[0], view=page_view)
        page_view.message = message


def setup(bot: commands.Bot):
    bot.add_cog(Commands(bot))
