import discord
from discord.ext import commands
from discord.ext.commands import command


class Errors(commands.Cog):
    """Handles errors."""
    def __init__(self, stonks):
        self.stonks = stonks

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        default_error = (commands.NotOwner, commands.TooManyArguments, commands.MaxConcurrencyReached)
        if isinstance(error, default_error):
            message = f"Error has occurred: {error}"
        elif isinstance(error, commands.CommandNotFound):
            message = "Not valid command!"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = "Missing required argument!"
        elif isinstance(error, commands.MissingPermissions):
            message = "Permission denied!"
        elif isinstance(error, commands.DisabledCommand):
            message = f"{ctx.command} has been disabled!"
        else:
            message = f"Something went wrong! \"{error}\""

        await ctx.send(message, delete_after=30)


def setup(stonks):
    stonks.add_cog(Errors(stonks))
