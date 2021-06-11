import os
import discord
import logging

# basic running log that will sit on the server outside of docker /var/log/ausbot.log
# we can view this file anytime and keep an eye on errors or info
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
        filename="/var/log/ausbot.log", level=logging.INFO)
log = logging.getLogger(__name__)
discord_log = logging.getLogger('discord')
discord_log.setLevel(logging.ERROR)

# discord bots are event based programming, everything is built on predetermined events like "on_ready"
# we redefine what the bot will do with these events by overriding the functions
class AusBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_emote = discord.PartialEmoji(name="✅")
        self.file_storage = "/var/storage/gallery/"

    async def star_handler(self, payload):
        try:
            guild = self.get_guild(payload.guild_id)
            if guild is None:
                log.error('on_raw_reaction_add,unable to retrieve guild,{0}'.format(payload.guild_id))
                return
            channel = guild.get_channel(payload.channel_id)
            if channel is None:
                log.error('on_raw_reaction_add,unable to retrieve channel,{0}'.format(payload.channel_id))
                return
            message = await channel.fetch_message(payload.message_id)
            # this scans the message.reactions[] for a reaction that matches our star emote
            stars = next((x for x in message.reactions if str(x.emoji) == "⭐"),None)
            if stars is None:
                log.debug('on_raw_reaction_add,message does not contain favorite_emote,{0}'.format(payload.message_id))
                return
            if stars.count == 5:
                file_name_list = []
                for a in message.attachments:
                    file_name = "{0}{1}.{2}".format(self.file_storage, message.id, a.filename)
                    file_name_list.append(file_name)
                    await a.save(file_name)
                await message.add_reaction(self.check_emote)
                log.info('saved {0} to ausclan gallery'.format(",".join(file_name_list)))
        # handles exceptions for get_channel and fetch_message and save
        except Exception as e:
            log.error(e)
        pass

    # this executes when the bot has finished loading all of the configs and has established a connection
    # changing presence allows us to set a status on the bots profile
    async def on_ready(self):
        try:
            await client.change_presence(activity=discord.Game(name="Welcome"))
            log.info('on_ready,presence state set')
        except Exception as e:
            log.error(e)
        pass


    # this event happens when anyone adds a reaction to any message, we're going to check and see if its a star emote
    # and has at least 5 of them, then we will save the file to the server and use it in the websites gallery at /var/storage/gallery
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        # dont react to emotes the bot adds to messages
        if payload.member == client.user:
            return
        if payload.emoji != "⭐":
            await self.star_handler(payload)

# this intent is needed to retrieve the reaction data,
# its a configuration for discord approvals
intents = discord.Intents.default()
intents.members = True
intents.reactions = True

# we pull the botkey from the servers environment
# variables to prevent storing it in github
client = AusBot(intents=intents)
client.run(str(os.environ['DISCORD_BOTKEY']))
