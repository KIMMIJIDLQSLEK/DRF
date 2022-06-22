from rest_framework import serializers
from .models import User,UserProfile,Hobby

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        #serializer에서 사용할 model, field지정
        model=User
        fields=["id","username","email","password","fullname"]
        #password는 쓰기 전용(읽을수없음)
        extra_kwargs={
            'password':
                {'write_only':True}
        }