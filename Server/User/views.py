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
            print("username: " + username + "  password: " + password)
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        result = isUserAndPasswordCorrect(username, password)
        resultJsonData["response_code"] = result["response_code"]
        return JsonResponse(resultJsonData)
        # users = findUserByName(username)
        # if (len(users) == 0):
        #     resultJsonData["response_code"] = 3
        #     return JsonResponse(resultJsonData)

        # if (isPasswordCorrect(users[0], password)):
        #     resultJsonData["response_code"] = 0
        # else:
        #     resultJsonData["response_code"] = 4
        # return JsonResponse(resultJsonData)

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
            print("username: " + username + "  password: " + password)
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        users = findUserByName(username)
        if (len(users) != 0):
            resultJsonData["response_code"] = 3
            return JsonResponse(resultJsonData)

        hashPassword = getHashPassword(password)
        print("hashPassword: " + hashPassword)

        newUser = User(username=username, password=hashPassword)
        newUser.save()
        resultJsonData["response_code"] = 0
        return JsonResponse(resultJsonData)

    else:
        resultJsonData["response_code"] = 6
        return JsonResponse(resultJsonData)


def findUserByName(username):
    user = list(User.objects.filter(username=username))
    print("userNumber: " + str(len(user)))
    return user

def isPasswordCorrect(user, password):
    return check_password(password, user.password)

def getHashPassword(password):
    return make_password(password)


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






# response_code
# 0       更新成功
# 1       newScore不是整数
# 2       参数不足或者参数格式错误
# 3       用户不存在
# 4       密码错误
# 5       应该使用GET方法
# 6       应该使用POST方法
# 7       更新失败，newScore没有超过数据库中的分数

@csrf_exempt
def updateScore(request):
    request.encoding = 'utf-8'
    resultJsonData = {}
    if (request.method == 'POST'):
        try:
            username = request.POST['username']
            password = request.POST['password']
            newScore = request.POST['newScore']
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
        except Exception as e:
            resultJsonData["response_code"] = 1
            return JsonResponse(resultJsonData)

        if (result["user"].score < newScore):
            result["user"].score = newScore
            result["user"].save()
            resultJsonData["response_code"] = 0
            return JsonResponse(resultJsonData)
        else:
            resultJsonData["response_code"] = 7
            resultJsonData["originScore"] = result["user"].score
            return JsonResponse(resultJsonData)
    else:
        resultJsonData["response_code"] = 6
        return JsonResponse(resultJsonData)