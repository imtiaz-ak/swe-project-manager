help_text = """
```type .commands for all the commands

public github repository: https://github.com/imtiaz-ak/swe-project-manager/```
"""

command_text = """
    > **Prefix:**
    > use prefix .
    > 
    > **Starting a project:**
    > .start <projectname> <repo1> <repo2> ....
    > enter the name of all the repos for the project you're creating.
    > 
    > **Adding developers to projects:**
    > .add <projectname> <developer's discord username> <developer's github username>.
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
    > **Assign developer to issue:**
    > .assign <discord username> <issue id>
    > 
    > **Refreshing a project:**
    > .refresh <projectname> -> checks github and trello to check if anything has been changed
    """