from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
        data = {
            "information": "success",
            "difficulty": difficulty,
            "questuonType": questuonType
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"information": "failure"})
    