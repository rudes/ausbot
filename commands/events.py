import random
import logging
import discord

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission

log = logging.getLogger(__name__)

class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="event",
            description="Create a clan event",
            options=[
                create_option(name="title",
                    description="Title of the event, something like \"Corp Mass\"",
                    option_type=SlashCommandOptionType.STRING,
                    required=True),
                create_option(name="when",
                    description="When the event takes place (in AEST) \"8pm\" or \"01/31 8pm\" for a different day",
                    option_type=SlashCommandOptionType.STRING,
                    required=True),
                create_option(name="description",
                    description="any other details you want to add",
                    option_type=SlashCommandOptionType.STRING,
                    required=False),
                ])
    async def _event(self, ctx: SlashContext, title: str, when: str, description: str):
        embed = discord.Embed(title="{0} @ {1}".format(title, when),
                color = random.randint(0, 0xffffff),
                description=description)
        embed.set_author(name=ctx.author.name,
                icon_url=str(ctx.author.avatar_url_as(static_format='png')))
        await ctx.send(embed=embed)
