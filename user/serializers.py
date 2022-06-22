from rest_framework import serializers
from .models import User,UserProfile,Hobby

class HobbySerializer(serializers.ModelSerializer):
    #내가 지정한 필드를 가져오고 싶다
    my_custom_field=serializers.SerializerMethodField()

    def get_my_custom_field(self,obj):
        #각 유저의 유저프로필에 있는 취미 class 객체 출력
        print(f"{obj}/{type(obj)}")
        return "my_custom_field"

    class Meta:
        model=Hobby
        fields=["name","my_custom_field"]

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