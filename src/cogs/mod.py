import discord
import json
from discord.ext import commands
from discord.ext.commands import command
from utility import setup

class Mod(commands.Cog):
    """Mod commands, needs admin permissions."""

    def __init__(self, bot):
        self.bot = bot
        self.last_msg = None

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.last_msg = message

    @command(help="Snipes last deleted message!", name="snipe")
    @commands.has_permissions(administrator=True)
    async def snipe(self, ctx: commands.Context):
        if not self.last_msg:
            await ctx.send("There is no message to snipe!")
            return

        author = self.last_msg.author
        content = self.last_msg.content
        emb = discord.Embed(title=f"Message from {author}", description=content)
        await ctx.send(embed=emb)

    @command(help="Kick player from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} kicked by {ctx.author}. [{reason}]")

    @command(help="Ban player from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} banned by {ctx.author}. [{reason}]")

    @command(help="Unban player from the server.")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member: discord.Member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} has been unbanned!")
                return

    @command(help="Clear chat messages, needs an amount.")
    @commands.has_permissions(manage_messages=True)
    async def clear_chat(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)

    @command(help="Change users nickname using nick.")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, nick):
        await member.edit(nick=nick)
        await ctx.send(f"Nickname was changed to {member.mention}!")

    @command(name="setprefix", help="Set servers prefix for commands",)
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix):
        setup.set_prefix(guild=str(ctx.guild.id), prefix=prefix)
        await ctx.send(f"Successfully changed the prefix to: {prefix}")

    @command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension.capitalize()} loaded!", delete_after=20)

    @command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, extension):
        if extension == "mod":
            await ctx.send("Can't unload mod extension!")
        else:
            self.bot.unload_extension(f"cogs.{extension.lower()}")
            await ctx.send(f"{extension.capitalize()} unloaded!", delete_after=20)

    @command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, extension):
        if extension == "all":
            self.bot.reload_all_cogs(ctx)
            await ctx.send("All reloaded!", delete_after=20)
        else:
            self.bot.unload_extension(f"cogs.{extension}")
            self.bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"{extension.capitalize()} reloaded!", delete_after=20)


def setup(bot):
    bot.add_cog(Mod(bot))
