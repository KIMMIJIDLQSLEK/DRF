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

        user = UserModel.objects.get(id=1)  #현재 AnonymousUser
        hobbys=HobbyModel.objects.all()
        # hobbys= user.userprofile.hobby.all()


        for hobby in hobbys:
            hobby_members=hobby.userprofile_set.exclude(user=user).annotate(username=F('user__username')).values_list('username',flat=True)
            hobby_members=list(hobby_members)
            # print(dir(user))
            print(f"hobby:{hobby.name}/hobby members:{hobby_members}")



        try:
            one_hobby,created=HobbyModel.objects.get_or_create(id="406")

        except HobbyModel.DoesNotExist:
            #object가 존재하지 않을때 이벤트
            return Response({'error': "존재하지 않는 hobby입니다."},status=status.HTTP_400_BAD_REQUEST)  #status클래스를 통해 가독성,생산성 좋아짐
            # return Response({'error': "존재하지 않는 hobby입니다."},status=400)

        return Response({'message':'get method!'})

    # def post(self,request):
    #     return Response({'message':'post method!'})
    #
    # def put(self,request):
    #     return Response({'message':'put method!'})
    #
    # def delete(self,request):
    #     return Response({'message':'delete method!'})