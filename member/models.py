from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=120, unique=True)
    password = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'members'