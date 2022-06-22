from rest_framework import serializers
from .models import User,UserProfile,Hobby

class HobbySerializer(serializers.ModelSerializer):
    #내가 지정한 필드를 가져오고 싶다
    same_hobby_user=serializers.SerializerMethodField()

    #같은 취미를 가진 유저들 출력할것
    def get_same_hobby_user(self,obj): #obj: 각 유저의 취미객체
        user_list=[]
        for user_profile in obj.userprofile_set.all():
            user_list.append(user_profile.user.fullname) #취미객체 역참조->userprofile_set/ userprofile의 정참조->user
        return user_list

    class Meta:
        model=Hobby
        fields=["name","same_hobby_user"]

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