from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import permissions
from rest_framework import status

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
        try:
            one_hobby,created=Hobby.objects.get_or_create(id="406")

            if created: #만들어야하면
                one_hobby.name="달리기"
                one_hobby.save()
                print("생성완료")
            else: #이미 존재하면
                print(one_hobby)

        except Hobby.DoesNotExist:
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