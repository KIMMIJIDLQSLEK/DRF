from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        user.set_password(password) #해쉬값으로 넣어줌
        user.save(using=self._db)
        return user

    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Create your models here.
class User(AbstractBaseUser):
    username=models.CharField("사용자계정",max_length=20,unique=True)
    email=models.EmailField("이메일",max_length=20)
    password=models.CharField("비밀번호",max_length=200)  #아직 해쉬값으로 들어가지 않음
    fullname=models.CharField("닉네임",max_length=20)
    join_date=models.DateTimeField("가입일자",auto_now_add=True)
    # permission_rank=models.IntegerField(default=0)

    # is_active가 False일 경우 계정이 비활성화됨
    #탈퇴여부로 많이 사용
    is_active = models.BooleanField(default=True)

    # is_staff에서 해당 값 사용
    # admin인지 확인하는 여부
    is_admin = models.BooleanField(default=False)

    # id로 사용 할 필드 지정.
    # 로그인 시 USERNAME_FIELD에 설정 된 필드와 password가 사용된다.
    USERNAME_FIELD = 'username'

    # user를 생성할 때 입력받은 필드 지정
    REQUIRED_FIELDS = []

    objects = UserManager()  # custom user 생성 시 필요

    def __str__(self):
        return self.username

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        return True

    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label):
        return True

    # admin 권한 설정
    @property
    def is_staff(self):
        return self.is_admin


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

