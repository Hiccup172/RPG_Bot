import discord
import json # is just a "better" dictionary
import random
import time
import adventure

#TODO
#be able to take away money, transfer money from a to b, clean up code, make the add_amount defalt to 10.

def write_to_json(data_dict: dict) -> None:
    with open("adventure.json", "w") as file:
        json.dump(data_dict, file, indent = 4)

def read_from_json() -> dict:
    with open("adventure.json", "r") as file:
        data = json.load(file)
    return data

def write_to_shop(data_dict: dict) -> None:
    with open("shop.json", "w") as file:
        json.dump(data_dict, file, indent = 4)

def read_from_shop() -> dict:
    with open("shop.json", "r") as file:
        data = json.load(file)
    return data

# def ensure_user_exists(user_id: int) -> dict:
#     user_id = str(user_id)
#     data = read_from_json()
#     if user_id not in data:
#         data[user_id] = 100
#         write_to_json(data)
#     return data



def check_balance(user_id: int) -> int:
    user_id = str(user_id)
    data = read_from_json()
    data = data[user_id]["base"]["money"]

    return data.get(user_id)
    
def double(user_id: int) -> int:
    user_id = str(user_id)
    data = read_from_json()
    data = data[user_id]["base"]["money"]
    if adventure.character_exist(user_id=user_id) == False:
        return "make a character"
    if random.randint(0, 1, 2) == 1:
        data *= 2
    else:
        data //= 2

    write_to_json(data)

    return f"now you have {data[user_id]}"

def add_money(user_id: int, amount) -> int:
    user_id = str(user_id)
    data = read_from_json()
    data[user_id]["base"]["money"] += amount
    write_to_json(data)
    return data[user_id]["base"]["money"]

def subtract_money(user_id: int, amount) -> int:
    user_id = str(user_id)
    data = read_from_json()
    data[user_id]["base"]["money"] -= amount
    write_to_json(data)
    return data[user_id]["base"]["money"]

def transfer_money(user_id1: int, user_id2: int, amount: int) -> tuple: #make this to the adventure json adn the rest
    if amount < 1:
        return "no you can't do that"
    data = read_from_json()
    if adventure.character_exist(user_id=user_id1) == False:
        return "make a character"
    if adventure.character_exist(user_id=user_id2) == False:
        return "this guy is not in the system"

    if data[str(user_id1)]["base"]["money"] < amount:
        return "you dont have enough money"
    a = add_money(user_id=user_id2, amount=amount) 
    b = subtract_money(user_id=user_id1, amount=amount) 

    return (b, a)

def buy_item(user_i: int, item: str) -> str:
    user_id = str(user_i)
    data = read_from_json()
    shop = read_from_shop()
    if item not in shop:
        return "this doesn't exist"
    elif data[user_id]["base"]["money"] < shop[item]["price"]:
        return "ur broke, get more money"
    else:
        
        data[user_id]["base"]["money"] -= shop[item]["price"]
        data[user_id]["inventory"][item] = shop[item]
        write_to_json(data)
        return "you baught it!"
        




def show_shop(): #fully finished
    outs = []
    shop = read_from_shop()
    count = 1
    out = discord.Embed(title="Oswald's Shop", description="this is what is in the shop", color=discord.Color.blue())
    for i in shop:

        out.add_field(name = shop[i]["name"], value= shop[i]["description"], inline=True)
        out.add_field(name = "price", value=shop[i]["price"], inline=True)
        out.add_field(name = "damage", value=shop[i]["damage"], inline=True)
        
        if count % 5 == 0 or i == len(shop) - 1:
            outs.append(out)
            out = discord.Embed(title="Oswald's Shop", description="This is what is in the shop", color=discord.Color.blue())
        count += 1
    outs.append(out)

    return outs












