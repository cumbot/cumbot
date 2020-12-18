import discord
from discord.ext import commands
import json
from json import JSONDecodeError
import os

#XXX TODO:
# 1.) (Change Prefix?) Unique prefix. What happens when multiple bots are on the
#       server and a user types !help?
#
# 2.) Before adding to quotes dict, make sure message isn't equivalent to others.
#
# 3.) Parse for endlines

qf = './quotes.json'

#If quotes is empty then append empty dict
if not os.path.exists(qf):
    os.mknod(qf)
    with open(qf,'w') as f:
        d = {}
        json.dump(d,f)

def append(filename,tit,dat):
    with open(qf, 'r+') as f:
        data = json.load(f)
        if tit in data:
            return "Title taken, try again with a new title."
        else:
            f.seek(0)
            data[tit] = dat
            json.dump(data,f)
            f.truncate()
            return "Quote added :D"

def search(filename, tit):
    with open(qf) as f:
        data = json.load(f)
    r = ''
    try:
        r=data[tit]
    except:
        r = "No quote found with that title."
    return r

#Declaring bot looking for ! commands
bot = commands.Bot(command_prefix=".")

#List all quotes
@bot.command(name='all')
async def all(ctx):
    with open(qf) as f:
        data = json.load(f)
    pretty = '```'
    for k,v in data.items():
        pretty += k + ': ' + v + '\n'
    pretty += '```'
    await ctx.channel.send(pretty)

#Function for adding title + text
@bot.command(name="qadd")
async def qadd(ctx,tit,*args):
    if len(args) == 0:
        await ctx.channel.send("Please add a title along with a quote. Example: !qadd title message here")
        return
    tot = ''
    for x in args:
        tot += x + ' '
    await ctx.channel.send(append(qf,str(tit), tot))
    
#Retrieving quote given a valid title 
@bot.command(name="quote")
async def quote(ctx, tit):
    try:
        await ctx.channel.send(search(qf,tit))
    except ValueError:
        await ctx.channel.send("Please add a title along with a quote. Example: !qadd title message here")


#insert your discord bot token here.
bot.run('')
