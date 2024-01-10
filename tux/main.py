# main.py
import os

import discord
from cog_loader import CogLoader
from discord.ext import commands
from dotenv import load_dotenv
from utils.tux_logger import TuxLogger

logger = TuxLogger(__name__)
load_dotenv()


async def setup(bot: commands.Bot, debug: bool = False):
    """
    Set up the bot including loading cogs and other necessary setup tasks.
    """
    await CogLoader.setup(bot, debug)
    logger.debug("Event handler setup completed.")


async def main():
    try:
        bot_prefix = ">"
        intents = discord.Intents.all()
        bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

        await setup(bot, debug=True)

        @bot.command(name="sync")
        @commands.has_permissions(administrator=True)
        async def sync(ctx: commands.Context):
            """Syncs the slash command tree. This command is only available to administrators.

            Args:
                ctx (commands.Context): The invocation context sent by the Discord API which contains information
                about the command and from where it was called.
            """  # noqa E501

            if ctx.guild:
                bot.tree.copy_global_to(guild=ctx.guild)
            await bot.tree.sync(guild=ctx.guild)
            logger.info(f"{ctx.author} synced the slash command tree.")

        @bot.command(name="clear")
        @commands.has_permissions(administrator=True)
        async def clear(ctx: commands.Context):
            """Clears the slash command tree. This command is only available to administrators.

            Args:
                ctx (commands.Context): The invocation context sent by the Discord API which contains information
                about the command and from where it was called.
            """  # noqa E501

            bot.tree.clear_commands(guild=ctx.guild)
            if ctx.guild:
                bot.tree.copy_global_to(guild=ctx.guild)
            await bot.tree.sync(guild=ctx.guild)
            logger.info(f"{ctx.author} cleared the slash command tree.")

        @bot.event
        async def on_ready():
            """Called when the client is done preparing the data received from Discord. Usually after login is successful and the Client.guilds and co. are filled up.

            Note:
                This function is not guaranteed to be the first event called. Likewise, this function is not guaranteed to only be called once. This library implements reconnection logic and thus will end up calling this event whenever a RESUME request fails.

            https://discordpy.readthedocs.io/en/stable/api.html#discord.on_ready
            """  # noqa E501
            logger.info(f"{bot.user} has connected to Discord!", __name__)

            # Set the bot's status
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="All Things Linux",
                )
            )

        await bot.start(os.getenv("TOKEN") or "", reconnect=True)
    except Exception as e:
        logger.error(f"An error occurred while running the bot: {e}")


if __name__ == "__main__":
    import asyncio

    # Run the main function
    asyncio.run(main())
