from disnake.ext import commands, tasks
from loguru import logger

from bot import MyBot

class Tasks(commands.Cog):
    """An example cog to create scheduled background tasks.
       
       This class uses disnake's tasks.
       https://docs.disnake.dev/en/latest/ext/tasks/index.html
    """
    def __init__(self, bot: commands.Bot):
        self.bot: MyBot = bot
        self.clean_temp_dir.start()

    @tasks.loop(hours=1.0)
    async def clean_temp_dir(self):
        """ Clears all files from the bot's temporary directory. """
        # Don't execute the main task code on bot startup
        if self.clean_temp_dir.current_loop == 0:
            return
        
        logger.debug(f"Cleaning temp directory... [loop #{self.clean_temp_dir.current_loop}]")
        
        # Delete all files from the temporary directory
        self.bot.clear_temp_dir()
        logger.info("Finished clearing temp directory.")
    
    @clean_temp_dir.before_loop
    async def wait_before_tasks(self):
        await self.bot.wait_until_ready()

def setup(bot: commands.Bot):
    bot.add_cog(Tasks(bot))