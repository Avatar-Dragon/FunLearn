from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import json

from .models import User

# Create your views here.
def index(request):
    data = {"answer": "Hello, User!"}
    # return HttpResponse(simplejson.dumps(data, ensure_accii=False))
    return JsonResponse(data)


# 功能：用户登录
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
            print("username: " + username + "  password: " + password)
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        result = isUserAndPasswordCorrect(username, password)
        resultJsonData["response_code"] = result["response_code"]
        return JsonResponse(resultJsonData)

    else:
        resultJsonData["response_code"] = 6
        return JsonResponse(resultJsonData)



# 功能：用户注册
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
            print("username: " + username + "  password: " + password)
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        users = findUserByName(username)
        if (len(users) != 0):
            resultJsonData["response_code"] = 3
            return JsonResponse(resultJsonData)

        # 数据库应该保存密码的hash结果，而不是密码原文
        hashPassword = getHashPassword(password)
        print("hashPassword: " + hashPassword)

        # 将新用户记录到数据库中
        newUser = User(username=username, password=hashPassword)
        newUser.save()
        resultJsonData["response_code"] = 0
        return JsonResponse(resultJsonData)

    else:
        resultJsonData["response_code"] = 6
        return JsonResponse(resultJsonData)

# 通过用户名查找用户
def findUserByName(username):
    user = list(User.objects.filter(username=username))
    print("userNumber: " + str(len(user)))
    return user

# 检查密码是否正确
def isPasswordCorrect(user, password):
    return check_password(password, user.password)

# 获得hash密码
def getHashPassword(password):
    return make_password(password)

# 验证用户，检查用户名和密码是否同时存在并正确
# response_code
# 0       用户存在
# 3       用户不存在
# 4       密码错误
def isUserAndPasswordCorrect(username, password):
    users = findUserByName(username)
    if (len(users) == 0):
        return {"response_code": 3}
    if (isPasswordCorrect(users[0], password)):
        return {"response_code": 0, "user": users[0]}
    else:
        return {"response_code": 4}



# 查询用户的总得分
# response_code
# 0       查询成功
# 1       
# 2       参数不足或者参数格式错误
# 3       用户不存在
# 4       密码错误
# 5       应该使用GET方法
# 6       应该使用POST方法
@csrf_exempt
def getScore(request):
    request.encoding = 'utf-8'
    resultJsonData = {}
    if (request.method == 'POST'):
        try:
            username = request.POST['username']
            password = request.POST['password']
            print("username: " + username + "  password: " + password)
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        # 验证用户
        result = isUserAndPasswordCorrect(username, password)
        if (result["response_code"] != 0):
            resultJsonData["response_code"] = result["response_code"]
            return JsonResponse(resultJsonData)

        resultJsonData["response_code"] = 0
        resultJsonData["score"] = result["user"].score
        return JsonResponse(resultJsonData)
    else:
        resultJsonData["response_code"] = 6
        return JsonResponse(resultJsonData)





# 更新用户的总得分
# response_code
# 0       更新成功
# 1       更新失败，newScore、correctNumber或者wrongNumber不是整数
# 2       参数不足或者参数格式错误
# 3       用户不存在
# 4       密码错误
# 5       应该使用GET方法
# 6       应该使用POST方法
# 7       更新失败，newScore小于数据库中的分数
# 8       更新失败，correctNumber或者wrongNumber不是非负整数
@csrf_exempt
def updateScore(request):
    request.encoding = 'utf-8'
    resultJsonData = {}
    if (request.method == 'POST'):
        try:
            username = request.POST['username']
            password = request.POST['password']
            newScore = request.POST['newScore']
            correctNumber = request.POST['correctNumber']
            wrongNumber = request.POST['wrongNumber']
            print("username: " + username + "  password: " + password + "  newScore: " + newScore)
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        result = isUserAndPasswordCorrect(username, password)
        if (result["response_code"] != 0):
            resultJsonData["response_code"] = result["response_code"]
            return JsonResponse(resultJsonData)

        try:
            newScore = int(newScore)
            correctNumber  = int(correctNumber)
            wrongNumber  = int(wrongNumber)
        except Exception as e:
            resultJsonData["response_code"] = 1
            return JsonResponse(resultJsonData)

        # 如果新的分数小于旧分数，不会更新分数
        if (result["user"].score <= newScore):
            # 只有correctNumber和wrongNumber都是非负整数，才会更新分数、correctNumber和wrongNumber
            if (correctNumber >= 0 and wrongNumber >= 0):
                result["user"].score = newScore
                result["user"].correctNumber += correctNumber
                result["user"].wrongNumber += wrongNumber
                result["user"].save()
                resultJsonData["response_code"] = 0
                return JsonResponse(resultJsonData)
            else:
                resultJsonData["response_code"] = 8
                return JsonResponse(resultJsonData)
        else:
            resultJsonData["response_code"] = 7
            resultJsonData["originScore"] = result["user"].score
            return JsonResponse(resultJsonData)
    else:
        resultJsonData["response_code"] = 6
        return JsonResponse(resultJsonData)


# 查询用户的用户信息
# response_code
# 0       查询成功
# 1       
# 2       参数不足或者参数格式错误
# 3       用户不存在
# 4       密码错误
# 5       应该使用GET方法
# 6       应该使用POST方法
@csrf_exempt
def getUserInformation(request):
    request.encoding = 'utf-8'
    resultJsonData = {}
    if (request.method == 'POST'):
        try:
            username = request.POST['username']
            password = request.POST['password']
            print("username: " + username + "  password: " + password)
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        # 验证用户
        result = isUserAndPasswordCorrect(username, password)
        if (result["response_code"] != 0):
            resultJsonData["response_code"] = result["response_code"]
            return JsonResponse(resultJsonData)

        resultJsonData["response_code"] = 0
        resultJsonData["user"] = result["user"].__dict__
        del resultJsonData["user"]["_state"]
        del resultJsonData["user"]["id"]
        del resultJsonData["user"]["password"]

        return JsonResponse(resultJsonData)
    else:
        resultJsonData["response_code"] = 6
        return JsonResponse(resultJsonData)