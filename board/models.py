from django.db import models

# Create your models here.
class Board(models.Model):
    num = models.IntegerField(verbose_name="글번호", null=False, unique=True) # 글번호
    writer = models.CharField(verbose_name="작성자", null=False, max_length=30) # 작성자
    subject = models.CharField(verbose_name="제목",null=False,max_length=100) # 제목
    passwd = models.CharField(verbose_name="비밀번호",null=False,max_length=20)# 비밀번호
    content = models.CharField(verbose_name= "내용",null=False, max_length=2000)# 내용                               
    readcount=models.IntegerField(verbose_name="조회수", default=0 ) # 조회수
    ref = models.IntegerField(verbose_name="그룹화아이디") # 그룹화아이디
    restep = models.IntegerField(verbose_name="글순서") # 글순서
    relevel = models.IntegerField(verbose_name = "글레벨") # 글레벨
    regdate = models.DateTimeField(auto_now_add=True, verbose_name="작성일", blank=True) # 작성일
    ip = models.CharField(verbose_name="IP", max_length=20)# IP
    