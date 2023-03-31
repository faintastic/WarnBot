# *-* Made with love | Developed by api#0003 | https://terrorist.bio/api *-* #

# Import PYPI modules
import sys
import fade
import time
import platform
import os
import requests
import discord
import datetime
import string
import random
import sqlite3
import json
import ctypes

from pystyle import *
from colorama import *

__start_time__ = datetime.datetime.now()
__version__ = "V1.0"

config = json.load(open("config.json"))
prefix = config['Main Config']['Prefix']
footer = config['Main Config']['Footer']

DB = sqlite3.connect("assets/db/main.db")
cur = DB.cursor()
ctxx = discord.ApplicationContext

class Definitions:
    def Sprint(text):
        TZ = f"{Fore.RESET}{Fore.LIGHTBLACK_EX}{datetime.datetime.now().strftime('%H:%M:%H')}{Fore.RESET}"
        print(
            f"{TZ} {Style.BRIGHT}{text}{Style.RESET_ALL}"
        )
    
    def GetUnixTimestamp():
        rz = int(time.time())
        return rz
    
    def CheckDB(key):
        if key: return True
        else: return False

    def Title(title):
        try:
            ctypes.windll.kernel32.SetConsoleTitleA(f"{title}")
        except:
            pass