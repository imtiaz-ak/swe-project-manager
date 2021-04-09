help_text = """
```two-face is a project management bot that makes it easier for teams of developers and business people to collaborate on a project. It tries to solve the communication gap between the two by letting both groups speak their own language on two different platforms (github & trello) and connects the two platforms.

type .commands for all the commands

public github repository: https://github.com/imtiaz-ak/swe-project-manager/```
"""

command_text = """
    > **Starting a project:**
    > .create <projectname> <repo1 link> <repo2 link> .... <github token>
    > enter the url of all the repos for the project you're creating with an account's github token at the end
    > 
    > **View and delete projects:**
    > .projects --> shows all the proojects in this server
    > .projects <projectname> --> shows info about the particular project
    > .project <projectname> delete --> deletes the particular project
    > 
    > **Adding developers to projects:**
    > .add <projectname> <developer's discord username> <developer's github username>.
    > 
    > **Connecting trello board to project:**
    > .trello <projectname> <trello board url> <trello token>
    > 
    > **Managing trello board's stories:**
    > .stories <projectname> -> View all stories for particular project
    > .stories <projectname> todo -> View all the stories for project with status todo
    > .stories <projectname> doing -> View all the stories for project with status doing
    > .stories <projectname> done -> View all the stories for project with status done
    > 
    > **Managing github's issues:**
    > .issues <projectname> -> View all the issues for particular repository
    > .issues <projectname> todo -> View all the issues for project with status todo
    > .issues <projectname> doing -> View all the issues for project with status doing
    > .issues <projectname> done -> View all the issues for project with status done
    > .issues <projectname> <status> <discord username> -> Shows issues assigned to that developer
    > 
    > **Connecting trello story to github's issues:**
    > .connect <projectname> <story_id> <issue_id> -> Connects the issue on github with the story on trello
    > 
    > **Assign developer to issue:**
    > .assign <discord username> <issue id>
    > 
    > **Refreshing a project:**
    > .refresh <projectname> -> checks github and trello to check if anything has been changed
    """