import os
import discord
from discord.ext import commands
from text import command_text, help_text
from github_helpers import *
from trello_helpers import *
from keep_alive import keep_alive

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship

engine = create_engine('sqlite:///data.db', echo=True)
session = sessionmaker(bind=engine)()

Base = declarative_base()

class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    github_token = Column(String)
    trello_url = Column(String)
    trello_token = Column(String)
    repositories = relationship('Repository', back_populates='project', cascade='all, delete')

    def __init__(self, name, github_token, trello_url=None, trello_token=None):
        self.name = name
        self.github_token = github_token
        self.trello_url = trello_url
        self.trello_token = trello_token

class Repository(Base):
    __tablename__ = 'repository'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship('Project', back_populates='repositories')

    def __init__(self, url, project):
        self.url = url
        self.project = project
        self.project_id = project.id

class Developer(Base):
    __tablename__ = 'developer'

    id = Column(Integer, primary_key=True)
    discord_username = Column(String)
    github_username = Column(String)

        
Base.metadata.create_all(engine)

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
        # add the project info in the database
        project = Project(name=project_name, github_token=args[-1])
        session.add(project)
        
        # add the info for each repo into the database
        for repo in repo_list:
            repository = Repository(url=repo, project=project)
            session.add(project)

        session.commit()
        await ctx.send("Added project '{}' with the given repository urls.".format(project_name))

@bot.command()
async def add(ctx, project_name, discord_username, github_username):
    if discord_username_exists(discord_username) and github_username_exists(github_username):
        # check if any project with the same name exists or not
        await ctx.send("Adding user {} with github username {} to project {}".format(discord_username, gitlab_username, project_name))
    else:
        await ctx.send("Could not add the user to the project '{}'. Please check if you've properly typed both the discord username and github username. Use .commands to view all the commands.".format(project_name))


@bot.command()
async def trello(ctx, project_name, trello_url, trello_token):
    pass

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