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
    hobby=HobbySerializer(many=True,required=False)  #hobby serializer 등록시키기 위해
    get_hobby=serializers.ListField(required=False) #받는 request.data의 get_hobby값 vaildator에 통과시키기 위해

    class Meta:
        model=UserProfile
        # fields="__all__"
        fields=["introduction","birthday","age","hobby","get_hobby"]

class UserSerializer(serializers.ModelSerializer):
    userprofile=UserProfileSerializer()

    #custom creator
    def create(self,validated_data):  #views에서 serializer.save하면서 validated_data 넘어감
        print(validated_data)

        userprofile=validated_data.pop("userprofile")
        get_hobby=userprofile.pop("get_hobby",[])

        #user object 생성
        user=User(**validated_data)
        user.save()

        #userprofile object 생성
        userprofile=UserProfile.objects.create(
            user=user,**userprofile
        )
        print("1")

        #hobby- userprofile에서 등록
        userprofile.hobby.add(*get_hobby) #manytomany이므로
        userprofile.save()

        return user

    #custom validator
    #Meta에서 검증하고 그다음 custom validator로 검증
    def validate(self,data):
        if data.get("userprofile",{}).get("age",'')<12:
            raise serializers.ValidationError(  #12세 이하이면 error띄우기
                detail={"error":"12세 이상만 가입할 수 있습니다."},
            )
        return data



    class Meta:
        #serializer에서 사용할 model, field지정
        model=User
        fields=["id","username","email","password","fullname","userprofile"]
        #password는 쓰기 전용(읽을수없음)
        extra_kwargs={
            'password':
                {'write_only':True},
            'email':{
                'error_messages':{
                    'required':'이메일을 입력해주세요.',
                    'invalid':'알맞은 형식의 이메일을 입력해주세요.',
                },
                'required':False #validator에서 검증여부 => False일경우 email error를 굳이 보여주지 않겠다.(default=True)
            },
        }