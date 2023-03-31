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

from discord.ext import commands
from pystyle import *
from assets.helpers.Definitions import *

# -- MAKE MOBILE STATUS (OPTIONAL) -- #
from discord.gateway import DiscordWebSocket, _log
async def MobileStatus(self):
    Payload = {
        'op': self.IDENTIFY,
        'd' : {
            'token': self.token,
            'properties': {
                '$os': sys.platform,
                '$browser': 'Discord Android',
                '$device': 'Discord Android',
                '$referrer': '',
                '$referring_domain': ''
            },
            'compress': True,
            'large_threshold': 250,
            'v': 3
        }
    }
    if self.shard_id is not None and self.shard_count is not None:
        Payload['d']['shard'] = [self.shard_id, self.shard_count]
    state = self._connection
    if state._activity is not None or state._status is not None:
        Payload['d']['presence'] = {
            'status': state._status,
            'game': state._activity,
            'since': 0,
            'afk': False
        }
    if state._intents is not None:
        Payload['d']['intents'] = state._intents.value
    await self.call_hooks('before_identify', self.shard_id, initial=self._initial_identify)
    await self.send_as_json(Payload)
    _log.info('Shard ID %s has sent the IDENTIFY payload.', self.shard_id)

# -- Initialze bot -- #
if config['Status Config']['Mobile status?']:
    DiscordWebSocket.identify = MobileStatus

client = commands.Bot(
    command_prefix = prefix,
    help_command   = None,
    intents        = discord.Intents.all()
)

# -- Start bot events -- #
@client.event
async def on_ready():
    if config['Status Config']['Mobile status?']:
        await client.change_presence(
            activity = discord.Activity(
                type = config['Status Config']['Activity type'],
                name = config['Status Config']['Status name']
            )
        )
    else:
        await client.change_presence(
            status = discord.Status.dnd,
            activity = discord.Activity(
                type = config['Status Config']['Activity type'],
                name = config['Status Config']['Status name']
            )
        )
    print(Colorate.Horizontal(Colors.blue_to_purple, f"""
 █████╗ ██████╗ ██╗ ██╗ ██╗  ██████╗  ██████╗  ██████╗ ██████╗ 
██╔══██╗██╔══██╗██║████████╗██╔═████╗██╔═████╗██╔═████╗╚════██╗
███████║██████╔╝██║╚██╔═██╔╝██║██╔██║██║██╔██║██║██╔██║ █████╔╝
██╔══██║██╔═══╝ ██║████████╗████╔╝██║████╔╝██║████╔╝██║ ╚═══██╗
██║  ██║██║     ██║╚██╔═██╔╝╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝
╚═╝  ╚═╝╚═╝     ╚═╝ ╚═╝ ╚═╝  ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Logged in as » {client.user} ({client.user.id})
Python version » {platform.python_version()}
OS information » {platform.system()} {platform.release()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""))
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS warns
    (userID INTEGER, username TEXT, userdiscrim TEXT, reason TEXT, timestamp TEXT, warnID TEXT, modID INTEGER, modusername TEXT, moddiscrim TEXT, guild INTEGER)
        """
    )
    DB.commit()

# -- Load cog files -- #
for folder in os.listdir("assets/cogs"):
    for module in os.listdir(f"assets/cogs"):
        if module.endswith(".py"):
            try:
                module_name = f"assets.cogs.{module[:-3]}"
                if module_name not in client.extensions:
                    client.load_extension(module_name)
                    Definitions.Sprint(f"Loaded module ~ {module_name}")
                else:
                    pass
            except Exception as error:
                Definitions.Sprint(f"Failed to load extension. Error: {error}")

# -- Start bot -- #
client.run(config['Main Config']['Token'])