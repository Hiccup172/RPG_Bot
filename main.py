import discord
from discord.ext import commands
import economy
import time
import adventure
import asyncio
from discord.ui import View, Button
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content=True 
description = ") aloooooooooooooooo bot"
bot = commands.Bot (command_prefix=')', description=description, intents=intents)
ttmoney = 0

@bot.event
async def on_ready():
    print('Logged in as') 
    print(bot.user.name)
    print(bot.user.id)
    print('----')
    game = discord.Game("Rizzing up eric")
    await bot.change_presence (status=discord.Status.online, activity=game)






@bot.command(name = "cash", description="shows how many coins you have")
async def cash(self, member: discord.Member = None):
    if member is None:
        member = self.author
    money = economy.check_balance(member.id)
    await self.send(f"you have {money} coins")

@bot.command(name = "gamble", description="doubles or halves your money")
async def d_or_h(self):
    if member is None:
        member = self.author
    money = economy.double(member)
    await self.send(f"now you have {money} coins")

@bot.command(name = "add_a", description="increases your money by a desired amount")
async def add_amount(self, amount:int):
    money = economy.add_money(self.author.id, amount)
    await self.send(f"now you have {money} coins")

@bot.command(name = "tfer", description="transfer a desired amount of money")
async def tfer(self, id2: discord.Member, amount:int):
    if not adventure.character_exist(self.author.id):
        await self.send("you have no character, go make one!!!")
        return
    id2 = id2 
    print(id2)
    result = economy.transfer_money(self.author.id, id2.id, amount)
    if isinstance(result, str):
        await self.send(result)
    else:
        await self.send(f"you now have {result[0]} and {id2.mention} has {result[1]}")

@bot.command(name = "create", description="the begining of your adventure, who you would like to be")
async def create_class(self):
    out = adventure.create_character(self.author.id)
    await self.send(f"you have made {out[0]}")

@bot.command(name = "delete", description="delete your charcter from the thing that i have storing it")
async def delete(self): 
    if not adventure.character_exist(self.author.id):
        await self.send("you have no character, go make one!!!")
        return
    
    out = adventure.ur_stats(user_id=self.author.id)
    await self.send(embed = out)


    def check(m):
        return m.author == self.message.author and m.channel == self.channel
    try:
        response = await bot.wait_for('message', check=check, timeout = 30)
    except asyncio.TimeoutError:
        await self.send("Took too long to choose.")
        return
    if response.content.lower() in ("yes", "y"):
        adventure.delete_character(user_id=self.author.id)
        await self.send("you deleted it")
    else:
        await self.send("it wasn't deleted try something that works")

@bot.command(name = "stat", description="here you check your stats")
async def stats(self):
    if not adventure.character_exist(self.author.id):
        await self.send("you have no character, go make one!!!")
        return
    user_id = self.author.id


    out = adventure.ur_stats(user_id=user_id)




    await self.send(embed = out)

@bot.command(name = "add", description="adds items this is a test will be removed for future")
async def add_item(self, item:str):
    if not adventure.character_exist(self.author.id):
        await self.send("you have no character, go make one!!!")
        return
    user_id = self.author.id
    await self.send(adventure.add_item(user_id=user_id, item=item))

#ryan was here

@bot.command(name = "sell", description="sells item from your inventory")
async def add_item(self, item:str):
    if not adventure.character_exist(self.author.id):
        await self.send("you have no character, go make one!!!")
        return
    user_id = self.author.id
    await self.send(adventure.remove_item(user_id=user_id, item=item))

@bot.command(name = "adv", description="you move on with your adventure", help="This command starts an adventure for the user. and you need to specify what weapon you are using") # DONE
async def adv(self, item: str = None):

    if item == None:
        await self.send("You need to specify what weapon you are using. Please use the command again and provide an item. like adv _____ (item)")
        return

    board= adventure.go_adventure(self.author.id, item)

    await self.send(board)



# @bot.command(name = "use", description="use an item, only in a battle state.")
# async def use(self, item): #work on me when you are done with adv


    await self.send(embed = adventure.action(user_id=self.author.id, item=item))

@bot.command(name = "up", description="CHEATER! though you leveled up")
async def up(self):
    adventure.leveling_up(self.author.id)
    x=adventure.read_from_json()
    x[str(self.author.id)]["base"]["level"]+=1
    adventure.write_to_json(x)
    await self.send("up")

@bot.command(name = "buy", description="you buy random things here, hope you find something you like")
async def buy(self, item):
    await self.send(economy.buy_item(self.author.id, item))

class ShopPaginator(View): # have no idea what this does but it works (the buttons)
    def __init__(self, embeds):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.current_page = 0

    async def update_message(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="First", style=discord.ButtonStyle.green)
    async def first_button(self, interaction: discord.Interaction, button: Button):
        self.current_page = 0
        await self.update_message(interaction)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.green)
    async def previous_button(self, interaction: discord.Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
        await self.update_message(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.green)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
        await self.update_message(interaction)

    @discord.ui.button(label="Last", style=discord.ButtonStyle.green)
    async def last_button(self, interaction: discord.Interaction, button: Button):
        self.current_page = len(self.embeds) - 1
        await self.update_message(interaction)

@bot.command(name = "shop", description="preview of shop") #fully finished
async def shop(self):
    embeds = economy.show_shop()
    pag = ShopPaginator(embeds)
    await self.send(embed=embeds[0], view=pag)

@bot.command(name = "heal", description="heals you to full use only once every 5 minutes")
async def heal(self):
    await self.send(adventure.daily_heal(self.author.id))



# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("You are missing a required argument.")
#     elif isinstance(error, commands.CommandNotFound):
#         await ctx.send("This command does not exist.")
#     elif isinstance(error, commands.BadArgument):
#         await ctx.send("You have provided an invalid argument.")
#     else:
#         await ctx.send("An error occurred: {}".format(str(error)))




bot.run('MTA4MDcwOTAwNDgyNjc4NzkyMg.GlWhkt.1MECs-EHnO_yAgsjlqCDVw_fJTmFOyVV9GQLwA')