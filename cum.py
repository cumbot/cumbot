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
pages = []
page_count = 0

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

@bot.command(name='rename')
async def rename(ctx,oldtit, newtit):
    r = ''
    with open(qf) as f:
        data = json.load(f)
    if newtit in data:
        r = "Title taken, try again with a new title."
    else:
        try:
            r = data[oldtit]
            data[newtit] = r
            del data[oldtit]
            with open(qf, 'w') as f:
                json.dump(data,f)
        except:
            r ="No quote found with that title."
    await ctx.channel.send(r)

#List all quotes
@bot.command(name='all')
async def all(ctx):
    with open(qf) as f:
        data = json.load(f)
    pretty = ''
    for k,v in data.items():
        pretty += k + ': ' + v + '\n'
    pretty += '```'

    pages_rows = pretty.split('\n')
    global pages
    pages = []
    mod = 1
    apnd = '```Page: 1 \n-------\n'
    pgnum = 2
    for x in pages_rows:
        apnd += x + '\n'
        if mod % 10 == 0:
            pages.append(apnd + '```')
            apnd = '```' + 'Page: ' + str(pgnum) + '\n-------\n'
            pgnum += 1
        elif mod == len(pages_rows):
            pages.append(apnd)
        mod += 1
    await ctx.channel.send(pages[0])
    msg = await ctx.channel.history(limit=1).flatten()
    msg = msg[0]
    await msg.add_reaction('\U000023EA')
    await msg.add_reaction('\U000023E9')


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

@bot.event
async def on_reaction_add(reaction,user):
    global pages
    global page_count
    if reaction.count >= 2 and str(reaction.emoji) == '\U000023EA':
        page_count += -1
        await reaction.message.edit(content=pages[page_count % len(pages)])
        
    elif reaction.count >= 2 and str(reaction.emoji) == '\U000023E9':
        page_count += 1
        await reaction.message.edit(content=pages[page_count % len(pages)])


#insert your discord bot token here.
bot.run('Nzg4NTAxNjM0NDk2ODU2MTI1.X9kbXw.ktg_XelyoPpeztxKZGRaVWLQxO0')
