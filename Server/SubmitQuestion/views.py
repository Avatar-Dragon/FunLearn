from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from User.views import isUserAndPasswordCorrect
from .models import SubmitMultipleQuestion, SubmitBooleanQuestion
from OpenTrivia.views import getCategoryByCode, convertBooleanQuestions, convertMultipleQuestions

# Create your views here.
def index(request):
    data = {"answer": "Hello, SubmitQuestion!"}
    # return HttpResponse(simplejson.dumps(data, ensure_accii=False))
    return JsonResponse(data)

# 功能：提交选择题
# response_code
# 0       正常访问
# 1       
# 2       参数不足或者参数格式错误
# 3       用户不存在
# 4       密码错误
# 5       应该使用GET方法
# 6       应该使用POST方法
# 7       已经存在类似问题
@csrf_exempt
def postMultipleQuestion(request):
    request.encoding = 'utf-8'
    resultJsonData = {}
    if (request.method == 'POST'):
        try:
            username = request.POST['username']
            password = request.POST['password']
            category = request.POST['category']
            difficulty = request.POST['difficulty']
            string_question = request.POST['string_question']
            correct_answer = request.POST['correct_answer']
            incorrect_answersA = request.POST['incorrect_answersA']
            incorrect_answersB = request.POST['incorrect_answersB']
            incorrect_answersC = request.POST['incorrect_answersC']
            print(username + " " + category + " " + difficulty + " " +
                string_question + " " + correct_answer + " " + 
                incorrect_answersA + " " + incorrect_answersB + " " + incorrect_answersC)
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        try:
            category = int(category)
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)
        
        # 判断category是否超过限定的范围
        category = getCategoryByCode(category)
        if (category == "NULL"):
            print("category error")
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        # 验证用户
        result = isUserAndPasswordCorrect(username, password)
        if (result["response_code"] != 0):
            resultJsonData["response_code"] = result["response_code"]
            return JsonResponse(resultJsonData)

        something, canCreate = SubmitMultipleQuestion.objects.get_or_create(
            category=category,
            difficulty=difficulty,
            string_question=string_question,
            correct_answer=correct_answer,
            incorrect_answersA=incorrect_answersA,
            incorrect_answersB=incorrect_answersB,
            incorrect_answersC=incorrect_answersC,
            user=result["user"])

        # 判断这条问题是否已经提交过了
        print("create multipleQuestion: " + str(canCreate))
        if (canCreate == False):
            resultJsonData["response_code"] = 7
            return JsonResponse(resultJsonData)

        resultJsonData["response_code"] = 0
        return JsonResponse(resultJsonData)
    else:
        resultJsonData["response_code"] = 6
        return JsonResponse(resultJsonData)


# 功能：提交判断题
# response_code
# 0       正常访问
# 1       
# 2       参数不足或者参数格式错误
# 3       用户不存在
# 4       密码错误
# 5       应该使用GET方法
# 6       应该使用POST方法
# 7       已经存在类似问题
@csrf_exempt
def postBooleanQuestion(request):
    request.encoding = 'utf-8'
    resultJsonData = {}
    if (request.method == 'POST'):
        try:
            username = request.POST['username']
            password = request.POST['password']
            category = request.POST['category']
            difficulty = request.POST['difficulty']
            string_question = request.POST['string_question']
            correct_answer = request.POST['correct_answer']
            incorrect_answers = request.POST['incorrect_answers']
            print(username + " " + category + " " + difficulty + " " +
                string_question + " " + correct_answer + " " + incorrect_answers)
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        try:
            category = int(category)
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)
        
        # 判断category是否超过限定的范围
        category = getCategoryByCode(category)
        if (category == "NULL"):
            print("category error")
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        # 验证用户
        result = isUserAndPasswordCorrect(username, password)
        if (result["response_code"] != 0):
            resultJsonData["response_code"] = result["response_code"]
            return JsonResponse(resultJsonData)

        something, canCreate = SubmitBooleanQuestion.objects.get_or_create(
            category=category,
            difficulty=difficulty,
            string_question=string_question,
            correct_answer=correct_answer,
            incorrect_answers=incorrect_answers,
            user=result["user"])

        # 判断这条问题是否已经提交过了
        print("create booleanQuestion: " + str(canCreate))
        if (canCreate == False):
            resultJsonData["response_code"] = 7
            return JsonResponse(resultJsonData)

        resultJsonData["response_code"] = 0
        return JsonResponse(resultJsonData)
    else:
        resultJsonData["response_code"] = 6
        return JsonResponse(resultJsonData)




# 功能：获得用户提交的题目
# response_code
# 0       正常访问
# 1       
# 2       参数不足或者参数格式错误
# 3       用户不存在
# 4       密码错误
# 5       应该使用GET方法
# 6       应该使用POST方法
@csrf_exempt
def getUserSubmitQuestion(request):
    request.encoding = 'utf-8'
    resultJsonData = {}
    if (request.method == 'POST'):
        try:
            username = request.POST['username']
            password = request.POST['password']
        except Exception as e:
            resultJsonData["response_code"] = 2
            return JsonResponse(resultJsonData)

        # 验证用户
        result = isUserAndPasswordCorrect(username, password)
        if (result["response_code"] != 0):
            resultJsonData["response_code"] = result["response_code"]
            return JsonResponse(resultJsonData)

        multipleQuestionResult = []
        booleanQuestionResult = []

        # 获取选择题
        multipleQuestionList = list(SubmitMultipleQuestion.objects.filter(user=result['user']))
        for item in multipleQuestionList:
            conItem = convertMultipleQuestions(item)
            conItem["permit"] = item.permit
            multipleQuestionResult.append(conItem)

        # 获取判断题
        booleanQuestionList = list(SubmitBooleanQuestion.objects.filter(user=result['user']))
        for item in booleanQuestionList:
            conItem = convertBooleanQuestions(item)
            conItem["permit"] = item.permit
            booleanQuestionResult.append(conItem)

        resultJsonData["response_code"] = 0
        resultJsonData["multipleQuestionResult"] = multipleQuestionResult
        resultJsonData["booleanQuestionResult"] = booleanQuestionResult
        return JsonResponse(resultJsonData)
    else:
        resultJsonData["response_code"] = 6
        return JsonResponse(resultJsonData)