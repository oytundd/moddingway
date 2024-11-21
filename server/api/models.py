from django.db import models


# Create your models here.
class User(models.Model):
    userid = models.IntegerField()
    discorduserid = models.CharField(max_length=20)
    discordguildid = models.CharField(max_length=20)
    ismod = models.BooleanField()

    def __str__(self) -> str:
        return str(self.userid)


class Exile(models.Model):
    exileid = models.IntegerField()
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    starttimestamp = models.DateTimeField()
    endtimestamp = models.DateTimeField()
    exilestats = models.IntegerField()

    def __str__(self) -> str:
        return f'User {self.userid} exiled for reason: "{self.reason}"'


class Strike(models.Model):
    strikeid = models.IntegerField()
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    createtimestamp = models.DateTimeField()

    def __str__(self) -> str:
        return f'User {self.userid} given strike for reason: "{self.reason}"'
