from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import urllib.request
from urllib.parse import urlencode
import json
import html.parser
import random

from .models import MultipleQuestion
from .models import BooleanQuestion

# Create your views here.
def index(request):
    data = {"answer": "Hello, OpenTrivia!"}
    # return HttpResponse(simplejson.dumps(data, ensure_accii=False))
    return JsonResponse(data)


# 获得一些question
def getQuestion(request):
    return getQuestionByAPI(request)

categoryMap = {
    "General Knowledge":                            9,
    "Entertainment: Books":                        10,
    "Entertainment: Film":                         11,
    "Entertainment: Music":                        12,
    "Entertainment: Musicals & Theatres":          13,
    "Entertainment: Television":                   14,
    "Entertainment: Video Games":                  15,
    "Entertainment: Board Games":                  16,
    "Science & Nature":                            17,
    "Science: Computers":                          18,
    "Science: Mathematics":                        19,
    "Mythology":                                   20,
    "Sports":                                      21,
    "Geography":                                   22,
    "History":                                     23,
    "Politics":                                    24,
    "Art":                                         25,
    "Celebrities":                                 26,
    "Animals":                                     27,
    "Vehicles":                                    28,
    "Entertainment: Comics":                       29,
    "Science: Gadgets":                            30,
    "Entertainment: Japanese Anime & Manga":       31,
    "Entertainment: Cartoon & Animations":         32
}

# 关于getQuestionByAPI的参数：

# category：
# "General Knowledge"                             9
# "Entertainment: Books"                         10
# "Entertainment: Film"                          11
# "Entertainment: Music"                         12
# "Entertainment: Musicals & Theatres"           13
# "Entertainment: Television"                    14
# "Entertainment: Video Games"                   15
# "Entertainment: Board Games"                   16
# "Science & Nature"                             17
# "Science: Computers"                           18
# "Science: Mathematics"                         19
# "Mythology"                                    20
# "Sports"                                       21
# "Geography"                                    22
# "History"                                      23
# "Politics"                                     24
# "Art"                                          25
# "Celebrities"                                  26
# "Animals"                                      27
# "Vehicles"                                     28
# "Entertainment: Comics"                        29
# "Science: Gadgets"                             30
# "Entertainment: Japanese Anime & Manga"        31
# "Entertainment: Cartoon & Animations"          32

# difficulty:
# medium
# easy
# hard

# type:
# multiple
# boolean

# response_code
# 0       正常访问
# 1       无法满足request，比如无法提供需要的题目
# 2       参数不足或者参数格式错误
# 3       服务器内部出错，访问url出现HTTPError
# 4       服务器内部出错，访问url出现URLError
# 5       应该使用GET方法
# 6       应该使用POST方法

# 通过访问https://opentdb.com/api.php提供的API来得到相应的question数据
def getQuestionByAPI(request):
    request.encoding = 'utf-8'
    resultJsonData = {}
    if (request.method == 'GET'):
        try:
            difficulty = request.GET['difficulty']
            questuonType = request.GET['questuonType']
            category = request.GET['category']
            amount = request.GET['amount']
        except Exception as e:
            resultJsonData["response_code"] = 2
            resultJsonData["results"] = []
            return JsonResponse(resultJsonData)

        # 将参数加入url
        questionUrl = "https://opentdb.com/api.php?amount=" + amount + "&category=" + category + "&difficulty=" + difficulty + "&type=" + questuonType
        print(questionUrl)

        try:
            oriData = urllib.request.urlopen(questionUrl).read()
        except urllib.request.HTTPError as e:
            print(e.code)
            # print(e.read())
            resultJsonData["response_code"] = 3
            resultJsonData["results"] = []
            return JsonResponse(resultJsonData)
        except urllib.request.URLError as e:
            print(str(e))
            resultJsonData["response_code"] = 4
            resultJsonData["results"] = []
            return JsonResponse(resultJsonData)

        # print(oriData)
        # url返回的数据是html格式，需要将其转换为Json（字典）格式
        jsonHttpData = json.loads(oriData)
        html_parser = html.parser.HTMLParser()
        oriJsonData = html_parser.unescape(jsonHttpData)
        print(oriJsonData['response_code'])

        resultJsonData = oriJsonData

        if (oriJsonData['response_code'] == 0):
            print("length: " + str(len(oriJsonData['results'])))
            return JsonResponse(resultJsonData)
        else:
            return JsonResponse(resultJsonData)

    else:
        resultJsonData["response_code"] = 5
        resultJsonData["results"] = []
        return JsonResponse(resultJsonData)
    


# response_code
# 0       正常访问
# 1       无法满足request，比如无法提供需要的题目
# 2       参数不足或者参数格式错误
# 3       服务器内部出错，访问url出现HTTPError
# 4       服务器内部出错，访问url出现URLError
# 5       应该使用GET方法
# 6       应该使用POST方法

# 通过访问https://opentdb.com/api.php提供的API来得到相应的question数据
def getQuestionInDatabase(request):
    request.encoding = 'utf-8'
    resultJsonData = {}
    if (request.method == 'GET'):
        try:
            difficulty = request.GET['difficulty']
            questuonType = request.GET['questuonType']
            category = request.GET['category']
            amount = request.GET['amount']
        except Exception as e:
            resultJsonData["response_code"] = 2
            resultJsonData["results"] = []
            return JsonResponse(resultJsonData)

        try:
            category = int(category)
            amount = int(amount)
        except Exception as e:
            resultJsonData["response_code"] = 2
            resultJsonData["results"] = []
            return JsonResponse(resultJsonData)

        if (questuonType == "multiple"):
            return JsonResponse(getSomeMultipleQuestionsRandom(difficulty, category, amount))
        elif (questuonType == "boolean"):
            return JsonResponse(getSomeBooleanQuestionsRandom(difficulty, category, amount))
        else:
            resultJsonData["response_code"] = 2
            resultJsonData["results"] = []
            return JsonResponse(resultJsonData)
    else:
        resultJsonData["response_code"] = 5
        resultJsonData["results"] = []
        return JsonResponse(resultJsonData)




# 将选择题数据从数据库格式转化为下列格式
def convertMultipleQuestions(item):
    return {
    "category": item.category,
    "type": "multiple",
    "difficulty": item.difficulty,
    "question": item.string_question,
    "correct_answer": item.correct_answer,
    "incorrect_answers": [item.incorrect_answersA, item.incorrect_answersB, item.incorrect_answersC]
    }


# 随机获得amount条选择题
def getSomeMultipleQuestionsRandom(difficulty, category, amount):
    results = []
    for i in categoryMap:
        if (categoryMap[i] == category):
            category = i
            break
    idList = list(MultipleQuestion.objects.values("id").filter(difficulty=difficulty, category=category))
    # print(idList)
    print("multipleQuestion length: " + str(len(idList)) + " amount: " + str(amount))
    if (len(idList) <= amount):
        oriDataList = list(MultipleQuestion.objects.filter(difficulty=difficulty, category=category))
        for item in oriDataList:
            results.append(convertMultipleQuestions(item))
        return {"response_code": 1, "results": results}
    else:
        finalIdList = random.sample(idList, amount)
        # print(finalIdList)
        for idItem in finalIdList:
            item = list(MultipleQuestion.objects.filter(id=idItem["id"]))[0]
            results.append(convertMultipleQuestions(item))
        return {"response_code": 0, "results": results}




# 将判断题数据从数据库格式转化为下列格式
def convertBooleanQuestions(item):
    return {
    "category": item.category,
    "type": "multiple",
    "difficulty": item.difficulty,
    "question": item.string_question,
    "correct_answer": item.correct_answer,
    "incorrect_answers": item.incorrect_answers
    }

# 随机获得amount条判断题
def getSomeBooleanQuestionsRandom(difficulty, category, amount):
    results = []
    for i in categoryMap:
        if (categoryMap[i] == category):
            category = i
            break
    idList = list(BooleanQuestion.objects.values("id").filter(difficulty=difficulty, category=category))
    # print(idList)
    print("booleanQuestion length: " + str(len(idList)) + " amount: " + str(amount))
    if (len(idList) <= amount):
        oriDataList = list(BooleanQuestion.objects.filter(difficulty=difficulty, category=category))
        for item in oriDataList:
            results.append(convertBooleanQuestions(item))
        return {"response_code": 1, "results": results}
    else:
        finalIdList = random.sample(idList, amount)
        # print(finalIdList)
        for idItem in finalIdList:
            item = list(BooleanQuestion.objects.filter(id=idItem["id"]))[0]
            results.append(convertBooleanQuestions(item))
        return {"response_code": 0, "results": results}