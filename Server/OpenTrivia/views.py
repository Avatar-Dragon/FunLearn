from django.shortcuts import render
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
    request.encoding = 'utf-8'
    # try:
    #     difficulty = request.GET['difficulty']
    #     questuonType = request.GET['questuonType']
    # except Exception as e:
    #     return JsonResponse({"information": "failure for request problem"})

    questionUrl = "https://opentdb.com/api.php?amount=10&category=23&difficulty=easy&type=multiple"
    print(questionUrl)

    try:
        oriData = urllib.request.urlopen(questionUrl).read()

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
    html_parser = html.parser.HTMLParser()
    unescaped = html_parser.unescape(jsonData)
    # return JsonResponse(jsonData)

    # finalData = {
    #     'sessionID': jsonData['sessionID'],
    #     'problem_id': jsonData['problems'][0]['problem_id'],
    #     'problem_image_url': jsonData['problems'][0]['problem_image'],
    #     'string_question': jsonData['problems'][0]['string_question']
    # }

    return JsonResponse(unescaped)