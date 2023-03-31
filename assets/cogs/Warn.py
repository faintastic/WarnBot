# *-* Made with love | Developed by api#0003 | https://terrorist.bio/api *-* #

# -- Import PYPI modules -- #
import discord
import asyncio
import platform
import random
import os
import io
import datetime
import json
import sys
import time
import uuid
import sqlite3
import re

from discord.ext import commands
from pystyle import *
from assets.helpers.Definitions import *

class WarnSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
    perms = config['Role Config']['Perms role ID']

    @commands.command(name="warn",
                      aliases = ['w'])
    @commands.has_role(perms)
    async def warn_p(self, 
                     ctx: commands.Context, 
                     member: discord.Member=None, 
                     *, 
                     reason: str=None):
        if member is None:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Invalid syntax",
                    color=0xFF0000,
                    description=f"**{ctx.author.mention} Improper usage of command** \n\n"
                                f"**> <> Required | [] Optional** \n"
                                f"__**Correct syntax: {prefix}warn <member> [reason]**__",
                    timestamp=datetime.datetime.now()
                ).set_footer(text=footer)
            )
        

        if member == self.client.user:
            return await ctx.reply("Is this really how you feel about me? Wow :cry:")

        if member.bot:
            return await ctx.reply("Silly goose.. You can't warn a bot :skull:")

        if member == ctx.author:
            return await ctx.reply("Now why would you want to warn yourself?")
        
        warn_id = str(uuid.uuid4())
        timestamp = f"<t:{Definitions.GetUnixTimestamp()}:R>"

        if reason is None:
            reason = "No reason provided."

        try:
            cur.execute(
                "INSERT INTO warns VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (member.id, 
                 member.name, 
                 member.discriminator, 
                 reason, 
                 timestamp,
                 warn_id, 
                 ctx.author.id, 
                 ctx.author.name, 
                 ctx.author.discriminator, 
                 ctx.guild.id,)
            )
            DB.commit()

            cur.execute(
                "SELECT * FROM warns WHERE userID = ? AND guild = ?",
                (member.id, ctx.guild.id,)
            )

            if not Definitions.CheckDB(cur.fetchone()):
                raise Exception("Failed to warn")

            await ctx.reply(
                embed=discord.Embed(
                    title="Successfully warned!",
                    color=discord.Color.green(),
                    description=f"**{ctx.author.mention} user has been warned {member.mention}** \n\n"
                                f"__**Warn information:**__ \n"
                                f"> **User » {member.mention}** \n"
                                f"> **Warn ID » {warn_id}** \n"
                                f"> **Timestamp » <t:{Definitions.GetUnixTimestamp()}:R>** \n"
                                f"> **Reason » {reason}** \n"
                                f"> **Warned by » {ctx.author.mention}**",
                    timestamp=datetime.datetime.now()
                ).set_footer(text=footer)
            )
        except Exception as e:
            await ctx.reply(
                embed=discord.Embed(
                    title="Failed to warn",
                    color=discord.Color.red(),
                    description=f"**{ctx.author.mention} failed to warn user {member.mention}**",
                    timestamp=datetime.datetime.now()
                ).set_footer(text=footer)
            )
    @warn_p.error
    async def warn_p_error(self,
                           ctx:ctxx,
                           error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(
                embed = discord.Embed(
                    title = "Insufficent permissions",
                    color = 0xFF0000,
                    description = 
                                f"**{ctx.author.mention} you do not have the required role to run this command** \n\n"
                                f"**The required role is: <@&{WarnSystem.perms}>**",
                    timestamp = datetime.datetime.now()
                ).set_footer(
                    text = footer
                )
            )
    # TODO | Add a slash command version of {prefix}warn

    @commands.command(name="rwarn",
                      aliases = ['removewarn', 'r'])
    @commands.has_role(perms)
    async def rwarn_p(self, 
                      ctx: commands.Context, 
                      *, 
                      inpp: str=None):
        regex = re.compile('^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[8|9|aA|bB][0-9a-f]{3}-[0-9a-f]{12}$')
        if inpp is None:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Invalid syntax",
                    color=0xFF0000,
                    description=f"**{ctx.author.mention} Improper usage of command** \n\n"
                                f"**> <> Required | [] Optional** \n"
                                f"__**Correct syntax: {prefix}rwarn <input (member mention, warnid)>**__",
                    timestamp=datetime.datetime.now()
                ).set_footer(text=footer)
            )
        parts = inpp.split(" ")
        if len(parts) == 2:
            if (parts[1].lower() == "all" or parts[1].lower() == "clear") and (re.search("<@!?[0-9]+>", parts[0]) or parts[0].isdigit() or not parts[0].startswith("<@!")):
                cur.execute(
                    "DELETE FROM warns WHERE userID = ? AND guild = ?",
                    (int(re.sub("[^0-9]", "", parts[0])), ctx.guild.id,)
                )
                DB.commit()
                return await ctx.reply(
                    embed = discord.Embed(
                        title = "Successfully removed all warns",
                        color = 0x00FF00,
                        description = 
                                    f"**{ctx.author.mention} all warns for user {parts[0]} have been removed.**",
                        timestamp = datetime.datetime.now()
                    ).set_footer(
                        text = footer
                    )
                )
        search_via_uuid = False
        uuidd = None
        search_via_member = False
        member = None
        
        try:
            check = uuid.UUID(inpp, version=4)
            uuidd = str(check)
            search_via_uuid = True
        except ValueError:
            if regex.match(inpp):
                uuidd = str(inpp)
            else:
                try:
                    member = await commands.MemberConverter().convert(ctx, inpp)
                    search_via_member = True
                except commands.BadArgument:
                    return await ctx.reply(
                        embed=discord.Embed(
                            title="Invalid input",
                            color=0xFF0000,
                            description=f"**{ctx.author.mention} it seems your input doesn't contain a user mention, user id, username or a warn ID (OR IT IS INVALID)**",
                            timestamp=datetime.datetime.now()
                        ).set_footer(
                            text=footer
                        )
                    )
                    
        if search_via_uuid:
            cur.execute(
                "SELECT * FROM warns WHERE warnID = ? AND guild = ?",
                (uuidd, 
                 ctx.guild.id,)
            )
        elif search_via_member:
            cur.execute(
                "SELECT * FROM warns WHERE userID = ? AND guild = ?",
                (member.id, 
                 ctx.guild.id,)
            )

        if not Definitions.CheckDB(cur.fetchone()):
            return await ctx.reply(
                embed = discord.Embed(
                    title = "User has no warnings",
                    color = 0xFF0000,
                    description = 
                                f"**{ctx.author.mention} user has no warnings.**",
                    timestamp = datetime.datetime.now()
                ).set_footer(
                    text = footer
                )
            )
        if search_via_uuid:
            cur.execute(
                "DELETE FROM warns WHERE warnID = ? AND guild = ?",
                (uuidd, 
                 ctx.guild.id,)
            )
            DB.commit()
            cur.execute(
                "SELECT * FROM warns WHERE warnID = ? AND guild = ?",
                (uuidd, 
                 ctx.guild.id,)
            )
            return await ctx.reply(
                embed = discord.Embed(
                    title = "Successfully removed warn",
                    color = 0x00FF00,
                    description = 
                                f"**{ctx.author.mention} warn has been removed.**",
                    timestamp = datetime.datetime.now()
                ).set_footer(
                    text = footer
                )
            )
        elif search_via_member:
            cur.execute(
                "SELECT * FROM warns WHERE userID = ? AND guild = ?",
                (member.id, 
                 ctx.guild.id,)
            )

            warns = cur.fetchall()

            output_send = ""
            amount_of_warnings = 0
            for warn in warns:
                output_send += f"**ID: {warn[5]} | Moderator: {warn[7]}#{warn[8]}** \n{warn[3]} - {warn[4]} \n\n" 
                amount_of_warnings += 1

            await ctx.reply(
                embed = discord.Embed(
                    color = 0x00FF00,
                    description = 
                                f"__**You can only remove warns with their ID. (OR RUNNING {prefix}rwarn <member> all)**__\n\n"
                                f"{output_send}",
                    timestamp = datetime.datetime.now(),
                ).set_footer(
                    text = footer
                ).set_author(
                    icon_url = member.avatar.url,
                    name = f"{amount_of_warnings} Warnings for {member}"
                )
            )
    @rwarn_p.error
    async def rwarn_p_error(self,
                           ctx:ctxx,
                           error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(
                embed = discord.Embed(
                    title = "Insufficent permissions",
                    color = 0xFF0000,
                    description = 
                                f"**{ctx.author.mention} you do not have the required role to run this command** \n\n"
                                f"**The required role is: <@&{WarnSystem.perms}>**",
                    timestamp = datetime.datetime.now()
                ).set_footer(
                    text = footer
                )
            )
    # TODO | Add a slash command version of {prefix}rwarn

    @commands.command(name="lookup",
                    aliases=['l', 'warns', 'look'])
    @commands.has_role(perms)
    async def lookupp(self,
                    ctx: ctxx,
                    *,
                    inpp: str = None):
        if inpp is None:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Invalid syntax",
                    color=0xFF0000,
                    description=f"**{ctx.author.mention} Improper usage of command** \n\n"
                                f"**> <> Required | [] Optional** \n"
                                f"__**Correct syntax: {prefix}lookup <input (member mention)>**__",
                    timestamp=datetime.datetime.now()
                ).set_footer(text=footer)
            )
        user = None
        try:
            member = await commands.MemberConverter().convert(ctx, inpp)
            user = member
        except commands.BadArgument:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Invalid input",
                    color=0xFF0000,
                    description=f"**{ctx.author.mention} it seems your input doesn't contain a user mention, user id, or username (OR IT IS INVALID)**",
                    timestamp=datetime.datetime.now()
                ).set_footer(
                    text=footer
                )
            )

        cur.execute(
            "SELECT * FROM warns WHERE userID = ? AND guild = ?",
            (user.id,
            ctx.guild.id,)
        )
        warns = cur.fetchall()
        if not warns:
            return await ctx.reply(
                embed=discord.Embed(
                    title="User has no warnings",
                    color=0xFF0000,
                    description=
                    f"**{ctx.author.mention} user has no warnings.**",
                    timestamp=datetime.datetime.now()
                ).set_footer(
                    text=footer
                )
            )

        output_send = ""
        amount_of_warnings = 0
        for warn in warns:
            output_send += f"**ID: {warn[5]} | Moderator: {warn[7]}#{warn[8]}** \n{warn[3]} - {warn[4]} \n\n"
            amount_of_warnings += 1

        await ctx.reply(
            embed=discord.Embed(
                color=0x00FF00,
                description=
                f"__**You can only remove warns with their ID. (OR RUNNING {prefix}rwarn <member> all)**__\n\n"
                f"{output_send}",
                timestamp=datetime.datetime.now(),
            ).set_footer(
                text=footer
            ).set_author(
                icon_url=member.avatar.url,
                name=f"{amount_of_warnings} Warnings for {member}"
            )
        )
    @lookupp.error
    async def lookup_error(self,
                           ctx:ctxx,
                           error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(
                embed = discord.Embed(
                    title = "Insufficent permissions",
                    color = 0xFF0000,
                    description = 
                                f"**{ctx.author.mention} you do not have the required role to run this command** \n\n"
                                f"**The required role is: <@&{WarnSystem.perms}>**",
                    timestamp = datetime.datetime.now()
                ).set_footer(
                    text = footer
                )
            )
    # TODO | Add a slash command version of {prefix}lookup

    
def setup(client):
    client.add_cog(WarnSystem(client))