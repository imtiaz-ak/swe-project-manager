# Turn off bytecode generation
import sys

sys.dont_write_bytecode = True

# Django specific settings
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django

django.setup()

# Import your models for use in your script
from db.models import *
from asgiref.sync import sync_to_async

# Code for discord bot starts here
import os
import discord
from discord.ext import commands
from utils.text import command_text, help_text
from utils.github_helpers import *
from utils.trello_helpers import *
from utils.discord_helpers import *
from utils.keep_alive import keep_alive

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
async def create(ctx, project_name, *args):
    repo_list = []
    no_error = True

    for repo in args:

        # if its the last arg, its the token
        if repo == args[-1]:
            if not github_token_is_valid(repo):
                await ctx.send("Please enter a valid github token. Use the .commands to view the correct format.")
                break
        else:
            # otherwise, its a github repo link
            if github_repo_is_valid(repo):
                repo_list.append(repo)
            else:
                await ctx.send("Please enter valid github repository urls. Use the .commands to view the correct format.")
                break
    
    if no_error:
        # get the server id
        # add the project info in the database
        server_id = ctx.message.guild.id
        project_obj = Project.objects.create(name=project_name, server_id=server_id, github_token=args[-1])
        
        # add the info for each repo into the database
        for repo in repo_list:
            Repository.objects.create(url=repo, project_obj=project_obj)

        await ctx.send("Added project '{}' with the given repository urls.".format(project_name))

@bot.command()
async def projects(ctx, project_name=None, *args):
    server_id = ctx.message.guild.id
    if project_name is None:
        # show all the projects in this server
        projects = Project.objects.filter(server_id=server_id)
        
        if projects.exists():
            return_string = ""
            for p in projects:
                return_string += "{}\n".format(p.name)
            await ctx.send(return_string)
        else:
            await ctx.send("No projects available in this server.")

    else:
        # show the project with the right name from this server
        project_obj = Project.objects.filter(server_id=server_id, name=project_name)

        if not project_obj.exists():
            await ctx.send("No project with name '{}' exists in this server.".format(project_name))

        else:
            project_obj = Project.objects.get(server_id=server_id, name=project_name)
            if len(args) == 0:
                return_string = "Project Name: {}.\nThe developers on this project are:\n".format(project_name)
                for dev in DeveloperOnProject.objects.filter(project_obj=project_obj):
                    return_string += str(dev.developer_obj.github_username)
                await ctx.send(return_string)

            elif args[0] == 'delete':
                project_obj.delete()
                await ctx.send("Project '{}' has been deleted.".format(pr.nameoject_name))


@bot.command()
async def add(ctx, project_name, discord_username, github_username):
    server_id = ctx.message.guild.id
    if discord_username_exists(discord_username) and github_username_exists(github_username):
        # get or create the develoepr
        developer_obj, created = Developer.objects.get_or_create(discord_username=discord_username, server_id=server_id)
        if created:
            developer_obj.github_username = github_username
            developer_obj.save() 
        
        # check if the project exists or not
        project = Project.objects.filter(name=project_name, server_id=server_id)
        if not project.exists():
            await ctx.send("Project with name {} does not exist.".format(project_name))

        # check if the user is already added to the project or not
        else:
            developer_already_added = DeveloperOnProject.objects.filter(project_obj=project.first(), developer_obj=developer_obj)
            if developer_already_added:
                await ctx.send("This developer has been already added to this project.")
            else:
                DeveloperOnProject.objects.create(project_obj=project.first(), developer_obj=developer_obj)
                await ctx.send("Adding user {} with github username {} to project {}".format(discord_username, github_username, project_name))
    else:
        await ctx.send("Could not add the user to the project '{}'. Please check if you've properly typed both the discord username and github username. Use .commands to view all the commands.".format(project_name))


@bot.command()
async def trello(ctx, project_name, trello_url, trello_token):
    server_id = ctx.message.guild.id
    if can_access_trello_board(trello_url, trello_token):
        # check if project already has a trello attached or not
        project = Project.objects.filter(server_id=server_id, project_name=project_name)
        if not project.exists():
            await ctx.send("Project with given name does not exist in this server.")
        else:
            if not project.first().trello_url == "":
                await ctx.send("Project already has a trello board added to it.")
            else:
                project_obj = project.first()
                project_obj.trello_url = trello_url
                project_obj.trello_token = trello_token
                project_obj.save()
                await ctx.send("Given trello board has been added to the project '{}'.".format(project_obj.name))
    else:
        await ctx.send("Can't add the trello board. Please check if the url and token are correct or not. Type .commands to view the full command list.")

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
async def connect(ctx, project_name, story_id, issue_id):
    await ctx.send("connected story with id {} to issue with id {} from the project {}".format(project_name, story_id, issue_id))

@bot.command()
async def assign(ctx, discord_username, issue_id):
    await ctx.send("assigned user {} to issue with id {}".format(discord_username, issue_id))

@bot.command()
async def refresh(ctx, project_name):
    await ctx.send("refreshed project {}".format(project_name))


keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)
