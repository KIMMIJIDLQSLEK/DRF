from rest_framework import serializers
from .models import User,UserProfile,Hobby
class HobbySerializer(serializers.ModelSerializer):

    class Meta:
        model=Hobby
        fields=["name"]

class UserProfileSerializer(serializers.ModelSerializer):
    hobby=HobbySerializer(many=True)
    class Meta:
        model=UserProfile
        # fields="__all__"
        fields=["introduction","birthday","age","hobby"]

class UserSerializer(serializers.ModelSerializer):
    userprofile=UserProfileSerializer()
    class Meta:
        #serializer에서 사용할 model, field지정
        model=User
        fields=["id","username","email","password","fullname","userprofile"]
        #password는 쓰기 전용(읽을수없음)
        extra_kwargs={
            'password':
                {'write_only':True}
        }