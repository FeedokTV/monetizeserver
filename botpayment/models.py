from django.db import models

# Create your models here.
class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=200)
    project_type = models.CharField(max_length=15)
    project_owner_id = models.IntegerField()
    expiration_date = models.DateField()
    is_paused = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projects'

class ProjectPasses(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_1'

