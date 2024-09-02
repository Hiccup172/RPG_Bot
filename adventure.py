"""
this is where all the adventure related things go,
come here to find it!!!
"""
import time
import random
import json
import discord
from typing import Union
from pprint import pprint
#class stats
#add the dictionary of the dictionarys in the hacker function and havethe loot pool, character can a thought on what you want to do for the future of this project.

def write_to_json(data_dict: dict) -> None:
    with open("adventure.json", "w") as file:
        json.dump(data_dict, file, indent = 4)

def read_from_json() -> dict:
    with open("adventure.json", "r") as file:
        data = json.load(file)
    return data

def read_from_lootpool() -> dict:
    with open("loot_pool.json", "r") as file:
        data = json.load(file)
    return data   

def read_job_template() -> dict:
    with open("job_template.json", "r") as file:
        data = json.load(file)
    return data

def read_from_creature() -> dict:
    with open("creatures.json", "r") as file:
        data = json.load(file)
    return data

def character_exist(user_id:int) -> bool:
    data = read_from_json()
    if str(user_id) not in data:
        return False
    return True


def create_character(user_id:int) -> tuple:
    data = read_from_json()

    if str(user_id) in data:
        print("you have created a character")
        return ("you already created a character",False)
    else:
        characters = read_job_template()
        
        data[user_id] = characters["human"]
        data[user_id]["inventory"] = {}
        data[user_id]["timers"] = {"daily_heal" : 0}

        write_to_json(data)
        print("create")
        return (f"you created your character as a human, you were supposed to choose, either i removed your choice or sometthing happened", True)

    

def delete_character(user_id:int) -> tuple:
    data = read_from_json()
    user_id = str(user_id)
    del data[user_id]
    write_to_json(data)

def check_stats(user_id:int) -> dict:
    data = read_from_json()
    user_id = str(user_id)
    return data[user_id]

def ur_stats(user_id:int):
    stat = check_stats(user_id=user_id)

    out = discord.Embed(title="your stats", description="you will see your stats here:", color=discord.Color.blue())
    out.add_field(name="level:",value=stat["base"]["level"],inline=True)
    out.add_field(name="xp:",value=stat["base"]["xp"],inline=True)
    out.add_field(name="hp:",value=stat["base"]["hp"],inline=True)
    inv = stat["inventory"]
    for i in inv:

        out.add_field(name = inv[i]["name"], value= inv[i]["description"], inline=True)
        
        out.add_field(name = "sell price", value=inv[i]["sell"], inline=True)
        out.add_field(name = "damage", value=inv[i]["damage"], inline=True)



#    out.add_field(name="strength:",value=stat["base"]["strength"],inline=True)
#    out.add_field(name="intelligence:",value=stat["base"]["intelligence"],inline=True)

#    out.add_field(name="hand:",value=stat["equiped"],inline=True)
    return out

def change_base_stats(user_id:int, amount:int, stat:str):
    user_id = str(user_id)
    data = read_from_json()
    data[user_id]["base"][stat] = int((1+data[user_id]["base"]["stat_for_levels"]) ** data[user_id]["base"][stat])
    write_to_json(data)
    return

def leveling_up(user_id:int):
    user_id = str(user_id)
    data = read_from_json()
    stat_list = ["max_hp"]

#    xp = 20 * (data[user_id]["base"]["stat_for_levels"] ** (data[user_id]["base"]["level"]-1))

    for stat in stat_list:
        change_base_stats(user_id=user_id, amount=5, stat = stat)
    return
 
def add_item(user_id:int, item:str):
    data = read_from_json()
    loot = read_from_lootpool()
    data[str(user_id)]["inventory"][item] = loot[item]
    write_to_json(data)
    return f"you added {item}"

def remove_item(user_id: int, item:str):
    data = read_from_json()
    if item not in data[str(user_id)]["inventory"]:
        return "you dont have this"
    data[str(user_id)]["base"]["money"]+= data[str(user_id)]["inventory"][item]["sell"]
    del data[str(user_id)]["inventory"][item]
    write_to_json(data)
    x = data[str(user_id)]["base"]["money"]
    return f"you sold {item} you have {x} coins now"

# def equipped(user_id: int, item:str): #useless but need for future maybe
#     data = read_from_json()
#     if item not in data[str(user_id)]["inventory"]:
#         return "you dont have this"
#     if data[str(user_id)]["inventory"][item]["location"] in data[str(user_id)]["item-equiped"]:
#         return "you alread have somthing here"
#     if data[str(user_id)]["inventory"][item]["requirement_in_strength"] > data[str(user_id)]["base"]["strength"]:
#         return "you are not strong enough to use this"
#     if data[str(user_id)]["inventory"][item]["requirement_in_intelligence"] > data[str(user_id)]["base"]["intelligence"]:
#         return "you are not smart enough to use this"
#     print(data[str(user_id)]["inventory"][item]["location"])
#     print(data[str(user_id)]["item-equiped"])


#     data[str(user_id)]["item-equiped"].append(data[str(user_id)]["inventory"][item]["location"])
#     data[str(user_id)]["equiped"][item] = data[str(user_id)]["inventory"][item]
#     del data[str(user_id)]["inventory"][item]
#     write_to_json(data)
#     return f"you equiped {item}"

# def unequip(user_id: int, item:str): #useless
#     data = read_from_json()
#     if item not in data[str(user_id)]["equiped"]:
#         return "you dont have this"
#     data[str(user_id)]["inventory"][item] = data[str(user_id)]["equiped"][item]
#     del data[str(user_id)]["equiped"][item]
#     data[str(user_id)]["item-equiped"].remove(data[str(user_id)]["inventory"][item]["location"])
#     write_to_json(data)
#     return f"you unequiped {item}"



def go_adventure(user_i: int, item: str): #DONE!!! well... not rly tho
    monsters = read_from_creature() #you can change what dificulty later also mind the S
    data = read_from_json()
    monster = random.choice(list(monsters))
    user_id = str(user_i)
    while monsters[monster]['level'] > data[user_id]["base"]["level"]:
        monster = random.choice(list(monsters))




    out = discord.Embed(title=monster, description="this is your enemy's stats", color=discord.Color.blue())
    out.add_field(name="dmg:",value=monsters[monster]["health"],inline=True)
    out.add_field(name="hp:",value=monsters[monster]["damage"],inline=True)
    out.add_field(name="xp:",value=monsters[monster]["xp"],inline=True)

    char_hp = data[user_id]["base"]["hp"]
    char_damage = data[user_id]["inventory"][item]["damage"] 
    char_xp = data[user_id]["base"]["xp"]
    
    monster_hp = monsters[monster]['health']
    monster_damage = monsters[monster]['damage']
    monster_xp = monsters[monster]['xp']
    monster_coins = monsters[monster]['coins']

    while char_hp > 0 and monster_hp > 0: 
        # Character attacks monster
        damage_dealt = random.randint(char_damage - 1, char_damage + 1)
        monster_hp -= damage_dealt

        if monster_hp <= 0:
            # Monster defeated
            data[user_id]["base"]["xp"] += monster_xp
            data[user_id]["base"]["hp"] = char_hp
            data[user_id]["base"]["money"] += monster_coins

            if data[user_id]["base"]["xp"] >= 20 * (data[user_id]["base"]["stat_for_levels"] ** (data[user_id]["base"]["level"]-1)): #level up system
                data[user_id]["base"]["level"] += 1
                data[user_id]["base"]["xp"] -= int(20 * (data[user_id]["base"]["stat_for_levels"] ** (data[user_id]["base"]["level"]-1)))
                lvl = data[user_id]["base"]["level"]
                leveling_up(user_id) # change how much to increase later
                write_to_json(data)
                if lvl%5==0:
                    return f"You defeated a {monster} and gained {monster_xp} XP. Your total XP is now {char_xp + monster_xp}. You have {char_hp} health left. and leveled up to {lvl}. the monsters you face may grow stronger..."
                return f"You defeated a {monster} and gained {monster_xp} XP. Your total XP is now {char_xp + monster_xp}. You have {char_hp} health left. and leveled up to {lvl}"
            write_to_json(data)
            return f"You defeated a {monster} and gained {monster_xp} XP. Your total XP is now {char_xp + monster_xp}. You have {char_hp} health left"
        
        # Monster attacks character
        damage_received = random.randint(monster_damage - 1, monster_damage + 1)
        char_hp -= damage_received
        if char_hp <= 0:
            # Character defeated
            data[user_id]["base"]["hp"] = 0
            data[user_id]["base"]["money"] -= 10
            write_to_json(data)
            return f"You were defeated by the monster. It was a {monster}. Luckly Steve found you while he was digging strait down, though of course, not for free, he took 10 coins... You may be at 0 health but you are still alive but unable to continue to continue adverturing, heal up to continue."
    
    return "Battle ended unexpectedly, or you have 0 hp"

# def if_dead(user_id : int):
    
    data = read_from_json()
    user_id_str = str(user_id)

    while True:
        decision = input("You are dead. Do you want to spend 50 gold to revive or restart with your current gold? (reply with 'revive' or 'restart'): ")

        if decision.lower() == 'revive':
            if data[user_id_str]["base"]["money"] >= 50:
                data[user_id_str]["base"]["money"] -= 50
                data[user_id_str]["base"]["hp"] = 100  # Revive with full health
                write_to_json(data)
                return f"You have been revived with 50 gold spent. You now have {data[user_id_str]['base']['money']} gold left."
            else:
                data[user_id_str]["base"]["hp"] = 100  # Restart with current gold but full health
                write_to_json(data)
                return "You don't have enough gold to revive. Restarting with your current gold."
        elif decision.lower() == 'restart':
            data[user_id_str]["base"]["hp"] = 100  # Restart with current gold but full health
            write_to_json(data)
            return f"You have restarted with your current gold. You now have {data[user_id_str]['base']['money']} gold."
        else:
            print("Invalid response. Please try again.")

def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1

    return

def daily_heal(user_id: int):
    user_id = str(user_id)
    data = read_from_json()

    current_time = time.time()
    cool_down = 300 #seconds
    last_heal = data[user_id]["timers"]["daily_heal"]

    if last_heal == 0 or (current_time-last_heal)>=cool_down:
        data[user_id]["base"]["hp"] = data[user_id]["base"]["max_hp"]
        data[user_id]["timers"]["daily_heal"] = int(current_time)
        write_to_json(data)
        return "you got healed fully"
    else:
        remaining_time = cool_down - (current_time - last_heal)
        minutes, seconds = divmod(int(remaining_time), 60)
        return f"you need to wait another {minutes} minutes and {seconds} seconds"






#print(go_adventure(709160342810525777))
# homework, equip unequip, stats are right, do equiping properly

#action("709160342810525777", "sword")
# if __name__ == "__main__":
#     delete_character("709160342810525777")

#leveling_up("709160342810525777")


    



