from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField("사용자계정",max_length=20,unique=True)
    email=models.EmailField("이메일",max_length=20,unique=True)
    password=models.CharField("비밀번호",max_length=60)
    fullname=models.CharField("닉네임",max_length=20)
    join_date=models.DateTimeField("가입일자",auto_now_add=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):  #User와 일대일관계/ Hobby와 다대다관계
    user=models.OneToOneField(to=User, verbose_name="사용자", on_delete=models.CASCADE)
    #OneToOne 필드가 어떤 형태인지
    #ManyToMany는 어떤 형태인지

    hobby=models.ManyToManyField(to="Hobby",verbose_name="취미") #Hobby클래스는 아래에 있으므로
    introduction= models.TextField("소개글")
    birthday=models.DateField("생일")
    age= models.IntegerField("나이")

    def __str__(self):
        return f"{self.user}의 profile"

class Hobby(models.Model):
    name=models.CharField("취미",max_length=50)

    def __str__(self):
        return self.name

