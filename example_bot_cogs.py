import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands

description = '''An example bot to showcase the discord.ext.commands extension
module. There are a number of utility commands being showcased here.'''

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PREFIX = os.getenv('PREFIX')

bot = commands.Bot(command_prefix=PREFIX)

initial_extensions = ['cogs.greetings']


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    # guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    # when using on_message it forbids any extra commands from running. using the below causes it to process commands
    await bot.process_commands(message)


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


'''
By Default, arguments to a Command function are strings. Therefore, we explicitly state that we expect the types to be int
'''


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='create-channel', help='Creates another channel named real-python. Requires admin role',
             pass_context=True)
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(error)
        await ctx.send('You do not have the correct role for this command.')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@bot.command(name='load', help='Loads an extension')
async def load(extension_name: str):
    """Loads an extension."""
    try:
        print(f'Loading extension {extension_name}.')
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))


@bot.command(name='unload', help='Unloads an extension')
async def unload(extension_name: str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))


if __name__ == "__main__":
    for extension in initial_extensions:
        try:
            print(f'Load extension {extension}.')
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.')

bot.run(TOKEN)
