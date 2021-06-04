import os
import discord
import logging

# basic running log that will sit on the server outside of docker /var/log/ausbot.log
# we can view this file anytime and keep an eye on errors or info
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)-8s %(message)s", filename="/var/log/ausbot.log")
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
discord_log = logging.getLogger('discord')
discord_log.setLevel(logging.WARNING)

# discord bots are event based programming, everything is built on predetermined events like "on_ready"
# we redefine what the bot will do with these events by overriding the functions
class AusBot(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.check_emote = discord.PartialEmoji(name="✅")
		self.file_storage = "/var/storage/gallery/"

	# this executes when the bot has finished loading all of the configs and has established a connection
	# changing presence allows us to set a status on the bots profile
	async def on_ready(self):
		await client.change_presence(activity=discord.Game(name="Welcome"))
		log.info('on_ready,presence state set')

	 # this event happens when anyone adds a reaction to any message, we're going to check and see if its a star emote
	 # and has at least 5 of them, then we will save the file to the server and use it in the websites gallery at /var/storage/gallery
	async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
		guild = self.get_guild(payload.guild_id)
		if guild is None:
			log.error('on_raw_reaction_add,unable to retrieve guild,{0}'.format(payload.guild_id))
			return
		try:
			channel = guild.get_channel(payload.channel_id)
			if channel is None:
				log.error('on_raw_reaction_add,unable to retrieve channel,{0}'.format(payload.channel_id))
				return
			message = await channel.fetch_message(payload.message_id)
			# this scans the message.reactions[] for a reaction that matches our star emote
			reaction = next((x for x in message.reactions if str(x.emoji) == "⭐"), None)
			if reaction is None:
				log.info('on_raw_reaction_add,message does not contain favorite_emote,{0}'.format(payload.message_id))
			if reaction.count > 4:
				await message.add_reaction(self.check_emote)
				await message.attachments[0].save(self.file_storage+message.filename)
				log.info('saved {0} to ausclan gallery'.format(message.filename))
		# handles exceptions for get_channel and fetch_message and save
		except (discord.NotFound, discord.Forbidden, discord.HTTPException, discord.InvalidArgument) as e:
			log.error('failed to pull file,{0}'.format(e.text))
		pass

# this intent is needed to retrieve the reaction data,
# its a configuration for discord approvals
intents = discord.Intents.default()
intents.members = True
intents.reactions = True

client = AusBot(intents=intents)
# we pull the botkey from the servers environment
# variables to prevent storing it in github
client.run(str(os.environ['DISCORD_BOTKEY']))