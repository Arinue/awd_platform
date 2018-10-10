from django.db import models
# Create your models here.

class Flag(models.Model):
    """
    靶机编号，靶机flag，flag入库时间，flag失效时间
    """
    target_num = models.CharField(max_length=10)
    flag_num = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)

class Flags(models.Model):
    """
    选手编号，提交flag，flag入库时间，flag失效时间
    """
    player_num = models.CharField(max_length=50)
    flag_num = models.CharField(max_length=50)

class Score(models.Model):
    """
    选手编号，选手分数，选手最后一次提交时间，选手的token值
    """
    player_num = models.CharField(max_length=10)
    fraction = models.IntegerField()
    last = models.DateTimeField(auto_now=True)
    flag_num = models.CharField(max_length=50)
    


class Logs(models.Model):
    """
    选手编号，提交的flag，flag提交时间，flag是否正确
    """
    player_num = models.CharField(max_length=10)
    flag_num = models.CharField(max_length=50)
    last = models.DateTimeField(auto_now_add=True)
    result = models.IntegerField()


class Status(models.Model):
    """
    靶机编号，选手编号，服务器是否正常运行
    """
    target_num = models.CharField(max_length=10)
    player_num = models.CharField(max_length=10)
    run = models.IntegerField()
