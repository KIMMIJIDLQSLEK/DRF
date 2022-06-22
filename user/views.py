from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import permissions
from rest_framework import status
from .models import UserProfile as UserProfileModel
from .models import Hobby as HobbyModel
from .models import User as UserModel
from django.db.models import F

from .serializers import UserSerializer,HobbySerializer
from django.contrib.auth import login
from django.conf import settings

#permission 커스텀
class MyGoodPermission(permissions.BasePermission):
    """
    Allow any access.
    This isn't strictly required, since you could use an empty
    permission_classes list, but it's useful because it makes the intention
    more explicit.
    """
    def has_permission(self, request, view):
        user=request.user
        result=bool(request.user and request.user.is_authenticated and user.permission_rank>5)
        return


#APIView를 사용하면 get, post, put, delete를 함수로 정의하여 사용할수있다.
class UserApiView(APIView):
    # permission_classes=[MyGoodPermission]
    permission_classes = [permissions.AllowAny] #누구나
    # permission_classes=[permissions.IsAdminUser] #admin일경우
    # permission_classes=[permissions.IsAuthenticated] #로그인한경우

    def get(self,request):
        '''
        #정참조
        userprofile=UserProfileModel.objects.get(id=1)
        print(userprofile.introduction)
        print(userprofile.age)

        #역참조
        hobby=HobbyModel.objects.get(id=1) #운동
        hobby_member=hobby.userprofile_set
        '''

        #모든 사용자에 대한 User와 UserProfile정보 가져오고
        # 같은 취미를 가진 사람들 출력-serializer에서 구한후 출력할것
        print("get method")
        user_serializer=UserSerializer(UserModel.objects.all(),many=True).data #쿼리셋일경우 many=True
        # hobby_serailizer=HobbySerializer(HobbyModel.objects.all(),many=True).data
        return Response(user_serializer,status=status.HTTP_200_OK)

    def post(self,request):
        print(request.data) #request형태 확인
        #validator
        '''
        사용자 정보를 입력받아 저장하는 함수
        '''
        #ToDo
        #request.data 가져옴->serializer형태로 저장할것이기 떄문에 받을때도 serializer형태로 받아야됨
        #가져온 data가 정상인지 확인/ 비정상일 경우 error보냄
        user_serializer=UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message':'정상'},status=status.HTTP_200_OK)

        return Response(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)