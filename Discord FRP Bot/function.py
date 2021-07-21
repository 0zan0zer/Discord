import discord
from random import randint as r
import re
import json


class Game:
    @staticmethod
    def roll_dice(x, y):
        return r(x, y)

    @staticmethod
    def get_digits(s):
        digits = []
        temp = ""
        symbols = ["+", "-", "/", "*", "x"]
        for key, i in enumerate(s):
            if i.isdigit() or i == "d":
                temp += i
                if len(s) - 1 == key:
                    digits.append(temp)
                    temp = ""
            elif not i.isdigit() or not i == "d":
                if i in symbols:
                    if temp == "":
                        temp = i
                    else:
                        digits.append(temp)
                        temp = i
                if not temp == "":
                    digits.append(temp)
                temp = ""
        return digits

    @staticmethod
    def is_dice(x):
        if "d" in x:
            return True
        else:
            return False

    @staticmethod
    def delete_d(x):
        temp = ""
        if "d" in x:
            for y in x:
                if y.isdigit():
                    temp += y
        return int(temp)

    @staticmethod
    def rollin_ds(s):
        game = Game()
        rolled = []
        for ele in s:
            if game.is_dice(ele):
                rolled.append(game.roll_dice(1, game.delete_d(ele)))
            else:
                rolled.append(ele)
        return rolled

    @staticmethod
    def math(s):
        res = s
        str1 = ""
        for ele in s:
            if isinstance(ele, int):
                str1 += str(ele)
            else:
                str1 += ele
        if "+" in str1 or "-" in str1:
            res = sum(map(int, re.findall(r'[+-]?\d+', str1)))
        return res

    @staticmethod
    async def create_data(users, user):
        if user.display_name not in users:
            roles = user.roles
            roles.reverse()
            top_role = roles[0]
            users[user.display_name] = {}
            users[user.display_name]["experience"] = 0
            users[user.display_name]["level"] = 1
            users[user.display_name]["class"] = f"{top_role}"
            users[user.display_name]["race"] = "Bilinmiyor"
            users[user.display_name]["desc"] = "Kim olduğu bilinmiyor"

    @staticmethod
    async def create_log(fight_log, amount, ctx):
        fight_log.clear()
        for i in range(amount):
            fight_log[i] = {}
            fight_log[i]["ctx"] = "---"
            fight_log[i]["name"] = ctx.author.display_name

    @staticmethod
    async def create_enemy(enemies, enemy_id, name, level, hp, mp):
        if name not in enemies:
            enemies[name] = {}
            enemies[name]["id"] = enemy_id
            enemies[name]["level"] = level
            enemies[name]["max_hp"] = hp
            enemies[name]["hp"] = hp
            enemies[name]["max_mp"] = mp
            enemies[name]["mp"] = mp

    @staticmethod
    async def update_data(users, user):
        roles = user.roles
        roles.reverse()
        top_role = roles[0]
        users[user.display_name]["class"] = f"{top_role}"

    @staticmethod
    async def set_race(users, user, race):
        users[user.display_name]["race"] = race

    @staticmethod
    async def set_desc(users, user, desc):
        users[user.display_name]["desc"] = desc

    @staticmethod
    def get_roll(args):
        game = Game()
        arg_list = []
        for arg in args:
            if arg != "roll":
                arg_list.append(arg)
        arg_str = ""
        for ele in arg_list:
            arg_str += ele
        switch = True
        for i in arg_str:
            if i == "d" or i == "+" or i == "-" or i.isdigit():
                continue
            else:
                switch = False
                break
        if switch:
            digits = game.get_digits(arg_str)
            rolled = game.rollin_ds(digits)
            sending_message = "%r= **[%s]**" % (rolled, game.math(rolled))
            if len(digits) == 1:
                bot_message = f"**{rolled}**"
            else:
                bot_message = sending_message
        else:
            bot_message = "Yanlış harf veya işaret kullandınız!"
        return bot_message

    @staticmethod
    def log_add(log_dir, name, ctx):
        log_len = len(log_dir) - 1
        for i in log_dir:
            if not int(str(i)) == log_len:
                log_dir[i]["ctx"] = log_dir[str(int(str(i)) + 1)]["ctx"]
                log_dir[i]["name"] = log_dir[str(int(str(i)) + 1)]["name"]
            else:
                log_dir[str(log_len)]["ctx"] = ctx
                log_dir[str(log_len)]["name"] = name
        return log_dir

    @staticmethod
    def get_colour_enemy(arg2):
        arg2 = int(arg2)
        enemy_colour = discord.Colour.light_gray()
        if arg2 > 9:
            if arg2 > 49:
                if arg2 > 99:
                    if arg2 > 499:
                        enemy_colour = discord.Colour.red()
                    else:
                        enemy_colour = discord.Colour.magenta()
                else:
                    enemy_colour = discord.Colour.blue()
            else:
                enemy_colour = discord.Colour.green()

        return enemy_colour

    @staticmethod
    def boss_bar(arg3):
        arg3 = int(arg3)
        return arg3 // 10

    @staticmethod
    async def attack_enemy(ctx, name, amount):
        game = Game()
        with open("Enemies.json", "r") as f:
            enemies = json.load(f)

        if name in enemies:
            enemies[name]["hp"] = enemies[name]["hp"] - amount
            if enemies[name]["hp"] > 0:
                enemy_colour = game.get_colour_enemy(enemies[name]["level"])
                hp = enemies[name]["max_hp"]
                mp = enemies[name]["max_mp"]
                bar_hp = game.boss_bar(enemies[name]["max_hp"])
                enemy_lvl = enemies[name]["level"]
                cur_hp = enemies[name]["hp"]
                cur_mp = enemies[name]["mp"]
                bar_cur_hp = game.boss_bar(cur_hp)
                bar_cur_mp = game.boss_bar(cur_mp)
                bar_black = bar_hp - bar_cur_hp

                embed = discord.Embed(
                    title=f"{name} LVL#{enemy_lvl}",
                    description=f"**HP: {hp}/{cur_hp}\nMP: {mp}/{cur_mp}**",
                    colour=enemy_colour
                )
                embed.add_field(
                    name="Bars",
                    value="**HP: **" + bar_cur_hp * ":red_square:" +
                          bar_black * ":black_large_square:" + "\n" +
                          "**MP: **" + bar_cur_mp * ":blue_square:",
                    inline=False
                )

                channel = ctx.channel
                msg = await channel.fetch_message(enemies[name]["id"])
                await msg.edit(embed=embed)

            elif enemies[name]["hp"] <= 0:
                channel = ctx.channel
                msg = await channel.fetch_message(enemies[name]["id"])
                await msg.delete()
                enemies.pop(name, None)

        with open("Enemies.json", "w") as f:
            json.dump(enemies, f, indent=2)
