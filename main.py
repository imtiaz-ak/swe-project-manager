import os
import discord
from discord.ext import commands
from text import command_text, help_text
from keep_alive import keep_alive

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def help(ctx):
    await ctx.send(help_text)

@bot.command()
async def commands(ctx):
    await ctx.send(command_text)

@bot.command()
async def start(ctx, project_name, *args):
    for repo in args:
        #ask for the link of the repos. carry out a convo here.
        pass
        
    await ctx.send("creating project")

@bot.command()
async def add(ctx, project_name, discord_username, gitlab_username):
    await ctx.send("adding user {} with gitlab username {} to project {}".format(discord_username, gitlab_username, project_name))

@bot.command()
async def stories(ctx, project_name, state='todo'):
    
    if state=='todo':
        await ctx.send("showing all the cards from project {} with state todo".format(project_name, state))
    
    if state=='doing':
        await ctx.send("showing all the cards from project {} with state doing".format(project_name, state))
    
    if state=='done':
        await ctx.send("showing all the cards from project {} with state done".format(project_name, state))
    
    await ctx.send("showing stories of the project")

@bot.command()
async def issues(ctx, project_name, state='todo', discord_username=None):
    if state=='todo':

        if discord_username is not None:
            await ctx.send("showing all the issues from project {} with state todo assigned to user {}".format(project_name, discord_username))    
        await ctx.send("showing all the issues from project {} with state todo".format(project_name, state))
    
    if state=='doing':

        if discord_username is not None:
            await ctx.send("showing all the issues from project {} with state doing assigned to user {}".format(project_name, discord_username))    
        await ctx.send("showing all the issues from project {} with state doing".format(project_name, state))

    if state=='done':

        if discord_username is not None:
            await ctx.send("showing all the issues from project {} with state done assigned to user {}".format(project_name, discord_username))    
        await ctx.send("showing all the issues from project {} with state done".format(project_name, state))
    
@bot.command()
async def assign(ctx, discord_username, issue_id):
    await ctx.send("assigned user {} to issue with id {}".format(discord_username, issue_id))

@bot.command()
async def refresh(ctx, project_name):
    await ctx.send("refreshed project {}".format(project_name))


keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)