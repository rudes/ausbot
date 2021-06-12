import os
import discord
import logging

from commands import events
from handlers import reactions

from discord.ext import commands
from discord_slash import SlashCommand

# basic running log that will sit on the server outside of docker /var/log/ausbot.log
# we can view this file anytime and keep an eye on errors or info
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
        filename="/var/log/ausbot.log", level=logging.INFO)
discord_log = logging.getLogger('discord')
discord_log.setLevel(logging.ERROR)
log = logging.getLogger(__name__)

# discord bots are event based programming, everything is built on predetermined events like "on_ready"
# we redefine what the bot will do with these events by overriding the functions
class AusBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # this executes when the bot has finished loading all of the configs and has established a connection
    # changing presence allows us to set a status on the bots profile
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await self.bot.change_presence(activity=discord.Game(name="Welcome"))
            log.info('on_ready,presence state set')
        except Exception as e:
            log.error(e)
        pass


# this intent is needed to retrieve the reaction data,
# its a configuration for discord approvals
intents = discord.Intents.default()
intents.members = True
intents.reactions = True

# create the bot and add the "Cogs" or classes
bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
bot.add_cog(AusBot(bot))
bot.add_cog(reactions.ReactionHandler(bot))
bot.add_cog(events.EventHandler(bot))

# we pull the botkey from the servers environment
# variables to prevent storing it in github
bot.run(str(os.environ['DISCORD_BOTKEY']))
