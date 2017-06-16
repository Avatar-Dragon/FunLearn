from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import urllib.request
from urllib.parse import urlencode
import json
import html.parser

# Create your views here.
def index(request):
    data = {"answer": "Hello, OpenTrivia!"}
    # return HttpResponse(simplejson.dumps(data, ensure_accii=False))
    return JsonResponse(data)



def getQuestion(request):
    return getQuestionByAPI(request)



# 关于getQuestionByAPI的参数：

# category：
# "General Knowledge"                        to     9
# "Entertainment: Books"                     to    10
# "Entertainment: Film"                      to    11
# "Entertainment: Music"                     to    12
# "Entertainment: Musicals & Theatres"       to    13
# "Entertainment: Television"                to    14
# "Entertainment: Video Games"               to    15
# "Entertainment: Board Games"               to    16
# "Science & Nature"                         to    17
# "Science: Computers"                       to    18
# "Science: Mathematics"                     to    19
# "Mythology"                                to    20
# "Sports"                                   to    21
# "Geography"                                to    22
# "History"                                  to    23
# "Politics"                                 to    24
# "Art"                                      to    25
# "Celebrities"                              to    26
# "Animals"                                  to    27
# "Vehicles"                                 to    28
# "Entertainment: Comics"                    to    29
# "Science: Gadgets"                         to    30
# "Entertainment: Japanese Anime & Manga"    to    31
# "Entertainment: Cartoon & Animations"      to    32

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
    