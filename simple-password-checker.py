import discord
from discord import app_commands
from discord.ext import commands, tasks
import math
import sys
import os


sys.stdout = sys.stderr
intents = discord.Intents.none()
client = commands.Bot(command_prefix = "/", intents = intents)
client.remove_command("help")


@client.event
async def on_ready():	
	change_status.start()


@tasks.loop(minutes = 5)
async def change_status():
	await client.change_presence(status = discord.Status.online,
								 activity=discord.Activity(
									type=discord.ActivityType.watching,
									name=f"in {len(client.guilds)} Servers"))


@client.tree.command(name = "ssc", description = "Syncronises the slash commands")
@app_commands.describe(ephemeral = "Should the use of this command be invisible to others?")
async def ssc(interaction: discord.Interaction, ephemeral: bool=True):
	await interaction.response.defer(thinking = True, ephemeral = ephemeral)
	if interaction.user.id in [1038916475525804123]:
		sync = await client.tree.sync()
		await interaction.followup.send(content = f"Synced {len(sync)} commands!")
	else:
		await interaction.followup.send(f"You do not have the permission to use this command", ephemeral = ephemeral)


@client.tree.command(name = "check", description = "Check your Password-Strength")
@app_commands.describe(digits = "How long is your password",
					   characters = "How many characters are checked - eg. 26 lowercase + 26 uppercase letters + 10 numbers = 62",
					   guessespers = "The amount of times the attacker tries to guess your password every second",
					   exactly = "Is it possible to enter less digits than the password is long?",
					   ephemeral = "Should the use of this command be invisible to others?")
async def check(interaction: discord.Interaction,
				digits: int,
				characters: int,
				guessespers: float,
				exactly: bool=True,
				ephemeral: bool=True):
	await interaction.response.defer(ephemeral = ephemeral, thinking = True)

	digits = int(digits)
	possibilities_1 = math.pow(characters, digits)
	possibilities_2 = 0
	if exactly == True:
			for power in range(1, digits):
				a = math.pow(10, power)
				possibilities_2 = possibilities_2 + a
	possibilities_3 = possibilities_1 + possibilities_2

	seconds = possibilities_3 / guessespers
	minutes = seconds / 60
	hours = minutes / 60
	days = hours / 24
	years = days / 365
	kiloyears = years / 1000
	megayears = kiloyears / 1000
	gigayears = megayears / 1000
	terayears = gigayears / 1000
	petayears = terayears / 1000

	check_embed_1 = discord.Embed(title = "__PASSWORD CHECK__", color = 0xfba422, description = "--------- INFO ---------")
	check_embed_2 = discord.Embed(color = 0xfba422, description = "--------- TIME ---------")
	check_embed_1.add_field(name = "Digits", value = f"{digits:,.0f}", inline = False)
	check_embed_1.add_field(name = "Guesses/s", value = f"{guessespers:,}", inline = False)
	check_embed_1.add_field(name = "Possible Characters", value = f"{characters:,.0f}", inline = False)
	check_embed_1.add_field(name = "Possibilities", value = f"{possibilities_3:,.0f}", inline = False)
	check_embed_2.add_field(name = "Seconds", value = f"{seconds:,.2f}", inline = False)
	if minutes >= 0.01:
		check_embed_2.add_field(name = "Minutes", value = f"{minutes:,.2f}", inline = False)
	if hours >= 0.01:
		check_embed_2.add_field(name = "Hours", value = f"{hours:,.2f}", inline = False)
	if days >= 0.01:
		check_embed_2.add_field(name = "Days", value = f"{days:,.2f}", inline = False)
	if years >= 0.01:
		check_embed_2.add_field(name = "Years", value = f"{years:,.2f}", inline = False)
	if kiloyears >= 0.01:
		check_embed_2.add_field(name = "Kiloyears", value = f"{kiloyears:,.2f}", inline = False)
	if megayears >= 0.01:
		check_embed_2.add_field(name = "Megayears", value = f"{megayears:,.2f}", inline = False)
	if gigayears >= 0.01:
		check_embed_2.add_field(name = "Gigayears", value = f"{gigayears:,.2f}", inline = False)
	if terayears >= 0.01:
		check_embed_2.add_field(name = "Terayears", value = f"{terayears:,.2f}", inline = False)
	if petayears >= 0.01:
		check_embed_2.add_field(name = "Petayears", value = f"{petayears:,.2f}", inline = False)
	check_embed_2.set_footer(text = "by Bliffbot#7080")
	await interaction.followup.send(embeds = [check_embed_1, check_embed_2], ephemeral = ephemeral)

client.run(os.environ["DISCORD_BOT_TOKEN"])