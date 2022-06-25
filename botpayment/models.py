from django.db import models

# Create your models here.
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=200)
    project_type = models.CharField(max_length=15)
    project_owner_id = models.IntegerField()
    expiration_date = models.DateField()
    is_paused = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projects'

class Ymbill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    bill_date = models.DateField()
    sender = models.BigIntegerField()
    withdraw = models.FloatField()
    extra_info = models.TextField()

    class Meta:
        managed = False
        db_table = 'ymbills'