from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password

from .models import User

# Create your views here.
def index(request):
    data = {"answer": "Hello, User!"}
    # return HttpResponse(simplejson.dumps(data, ensure_accii=False))
    return JsonResponse(data)


# response_code
# 0       正常访问
# 1       
# 2       参数不足或者参数格式错误
# 3       用户不存在
# 4       密码错误
# 5       应该使用GET方法
# 6       应该使用POST方法

@csrf_exempt
def login(request):
    request.encoding = 'utf-8'
    resultJsonData = {}
    if (request.method == 'POST'):
        try:
            username = request.POST['username']
            password = request.POST['password']
            print("username: " + username)
            print("password: " + password)
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        user = list(User.objects.filter(username=username))
        print("userNumber: " + str(len(user)))
        if (len(user) == 0):
            resultJsonData["response_code"] = 3
            return JsonResponse(resultJsonData)

        if (check_password(password, user[0].password)):
            resultJsonData["response_code"] = 0
        else:
            resultJsonData["response_code"] = 4
        return JsonResponse(resultJsonData)

    else:
        resultJsonData["response_code"] = 6
        return JsonResponse(resultJsonData)




# response_code
# 0       正常访问
# 1       
# 2       参数不足或者参数格式错误
# 3       用户已经存在
# 4       
# 5       应该使用GET方法
# 6       应该使用POST方法

@csrf_exempt
def register(request):
    request.encoding = 'utf-8'
    resultJsonData = {}
    if (request.method == 'POST'):
        try:
            username = request.POST['username']
            password = request.POST['password']
            print("username: " + username)
            print("password: " + password)
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        user = list(User.objects.filter(username=username))
        print("userNumber: " + str(len(user)))
        if (len(user) != 0):
            resultJsonData["response_code"] = 3
            return JsonResponse(resultJsonData)

        hashPassword = make_password(password)
        print("hashPassword: " + hashPassword)

        newUser = User(username=username, password=hashPassword)
        newUser.save()
        resultJsonData["response_code"] = 0
        return JsonResponse(resultJsonData)

    else:
        resultJsonData["response_code"] = 6
        return JsonResponse(resultJsonData)