import logging
import discord

log = logging.getLogger(__name__)

from discord.ext import commands

class ReactionHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_storage = "/var/storage/gallery/"
        self.check_emote = discord.PartialEmoji(name="✅")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # dont react to emotes the bot adds to messages
        if user == self.bot.user:
            return
        if reaction.emoji == "⭐":
            await self.star_handler(reaction,user)

    """
    this event happens when someone adds a star reaction to any message
    were going to see if they have 5 emotes
    then we will save the file to the server and use
    it in the websites gallery at /var/storage/gallery
    """
    async def star_handler(self, reaction, user):
        try:
            if reaction.count == 5:
                file_name_list = []
                for a in reaction.message.attachments:
                    # create a filename of self.filestorage/523453121452352535.filename.ext
                    file_name = "{0}{1}.{2}".format(self.file_storage,
                            reaction.message.id, a.filename)
                    file_name_list.append(file_name)
                    await a.save(file_name)
                await reaction.message.add_reaction(self.check_emote)
                log.info('saved {0} to ausclan gallery'.format(
                    ",".join(file_name_list)))
        except Exception as e:
            log.error(e)
        pass

