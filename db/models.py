import sys

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()


class Project(models.Model):

    class Meta:
        db_table = 'project'

    name = models.TextField()
    server_id = models.TextField()
    github_token = models.TextField()
    trello_url = models.TextField()
    trello_token = models.TextField()
    repositories = models.TextField()

class Repository(models.Model):
    
    class Meta:
        db_table = 'repository'
    
    url = models.TextField()
    project_obj = models.ForeignKey(Project, on_delete=models.CASCADE)


class Developer(models.Model):
    
    class Meta:
        db_table = 'developer'

    discord_username = models.TextField()
    github_username = models.TextField()
    server_id = models.TextField()

class DeveloperOnProject(models.Model):

    class Meta:
        db_table = 'developer_on_project'

    project_obj = models.ForeignKey(Project, on_delete=models.CASCADE)
    developer_obj = models.ForeignKey(Developer, on_delete=models.CASCADE)
    

