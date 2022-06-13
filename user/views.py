from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from .models import Hobby

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
        hobby_list=Hobby.objects.all() #queryset
        print(hobby_list)
        one_hobby=Hobby.objects.get(id=1) #object: 매칭되는게 무조건 하나여야함!!!
        print(one_hobby)
        filter_hobby=Hobby.objects.filter(id__gt=3)  #queryset: object의 집합(리스트의 형태)-아무것도 없어도 queryset
        print(filter_hobby)

        return Response({'message':'get method!'})

    # def post(self,request):
    #     return Response({'message':'post method!'})
    #
    # def put(self,request):
    #     return Response({'message':'put method!'})
    #
    # def delete(self,request):
    #     return Response({'message':'delete method!'})