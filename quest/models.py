from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=20,unique=True)
    email=models.EmailField(max_length=20,unique=True)
    password=models.CharField(max_length=60)
    fullname=models.CharField(max_length=20)
    join_date=models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):  #User와 일대일관계/ Hobby와 다대다관계
    user=models.OneToOneField(to=User, verbose_name="사용자", on_delete=models.CASCADE)
    hobby=models.ManyToManyField(to="Hobby",verbose_name="취미") #Hobby클래스는 아래에 있으므로
    introduction= models.TextField()
    birthday=models.DateField()
    age= models.IntegerField()

class Hobby(models.Model):
    name=models.CharField(max_length=50)

