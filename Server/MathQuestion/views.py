from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import urllib.request
from urllib.parse import urlencode
from urllib.request import ProxyHandler
import json
from http.cookiejar import Cookie, CookieJar
# from django.utils import simplejson
# import json

# Create your views here.
def index(request):
    data = {"answer": "Hello, MathQuestion!"}
    # return HttpResponse(simplejson.dumps(data, ensure_accii=False))
    return JsonResponse(data)

def getMathQuestion(request):
    request.encoding = 'utf-8'
    try:
        difficulty = request.GET['difficulty']
        questuonType = request.GET['questuonType']
    except Exception as e:
        return JsonResponse({"information": "failure for request problem"})

    questionUrl = "http://www5a.wolframalpha.com/input/wpg/problem.jsp?count=1&difficulty=" + difficulty + "&load=1&type=" + questuonType
    print(questionUrl)

    try:
        headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate, sdch",
            'Accept-Language': "zh-CN,zh;q=0.8",
            'Connection': "keep-alive",
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        req = urllib.request.Request(questionUrl, headers=headers)
        # oriData = urllib.request.urlopen(req).read()

        # 设置接受cookie
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        oriData = opener.open(req).read()

        # 打印cookie的各个值
        print(cj)
        for item in cj:
            print(item.version)
            print("Name: " + item.name)
            print("Vaule: " + item.value)
            print(item.port)
            print(item.port_specified)
            print(item.domain)
            print(item.domain_specified)
            print(item.domain_initial_dot)
            print(item.path)
            print(item.path_specified)
            print(item.secure)
            print(item.expires)
            print(item.discard)
            print(item.comment)
            print(item.comment_url)
            print(item.rfc2109)
            # print(item.httponly)

    except urllib.request.HTTPError as e:
        print(e.code)
        # print(e.read())
        return JsonResponse({"information": "failure for http"})
    except urllib.request.URLError as e:
        print(str(e))
        return JsonResponse({"information": "failure for url"})

    # checkUrl = "http://www5a.wolframalpha.com/input/wpg/checkanswer.jsp?attempt=1&difficulty=Beginner&load=true&problemID=MSP30821f17b43d8fie9ab40000452beg427da501bg&query=10&s=49&type=InputField"

    # print(oriData)
    jsonData = json.loads(oriData)
    # return JsonResponse(jsonData)

    finalData = {
        'sessionID': jsonData['sessionID'],
        'problem_id': jsonData['problems'][0]['problem_id'],
        'problem_image_url': jsonData['problems'][0]['problem_image'],
        'string_question': jsonData['problems'][0]['string_question']
    }

    return JsonResponse(finalData)


def checkAnswer(request):
    request.encoding = 'utf-8'
    try:
        problem_id = request.GET['problem_id']
        difficulty = request.GET['difficulty']
        query = request.GET['query']
        s = "49"
    except Exception as e:
        return JsonResponse({"information": "failure for check answer"})

    checkUrl = "http://www5a.wolframalpha.com/input/wpg/checkanswer.jsp?attempt=1&difficulty=" + difficulty + "&load=true&problemID=" + problem_id + "&query=" + query + "&s=" + s + "&type=InputField"
    print(checkUrl)

    try:
        headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate, sdch",
            'Accept-Language': "zh-CN,zh;q=0.8",
            'Connection': "keep-alive",
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            # 'Host': "www5a.wolframalpha.com",
            # 'Upgrade-Insecure-Requests': "1",
            # 'Cache-Control': "max-age=0"
        }
        # checkUrl = "http://www5a.wolframalpha.com/input/wpg/checkanswer.jsp?attempt=1&difficulty=Beginner&load=true&problemID=MSP30821f17b43d8fie9ab40000452beg427da501bg&query=1&s=49&type=InputField"
        req = urllib.request.Request(checkUrl, headers=headers)
        # oriData = urllib.request.urlopen(req).read()

        # 自定义2个cookie，信息来自getMathQuestion打印出来的信息
        c = Cookie(0, 'WR_SID', '120.236.174.172.1497365721706807', None, False, '.wolframalpha.com', True, True, '/', True, False, 1812725721, False, None, None, None)
        c2 = Cookie(0, 'JSESSIONID', '9EF3562A8408891A3958EDE4C5644E9C', None, False, 'www5a.wolframalpha.com', False, False, '/', True, False, None, True, None, None, None)
        cj2 = CookieJar()
        cj2.set_cookie(c)
        cj2.set_cookie(c2)
        print(cj2)

        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj2))
        oriData = opener.open(req).read()

    except urllib.request.HTTPError as e:
        print(e.code)
        # print(e.read())
        return JsonResponse({"information": "failure for http"})
    except urllib.request.URLError as e:
        print(str(e))
        return JsonResponse({"information": "failure for url"})

    return JsonResponse(json.loads(oriData))
