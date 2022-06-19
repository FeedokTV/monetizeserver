from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from requests import request as req
from botpayment.models import Projects


@csrf_exempt
def index(request : WSGIRequest):
    if request.method == 'GET':
        print('get')
        #r = req(method='POST', url='https://api.telegram.org/bot5527748790:AAFdKl6ySucQ_FQWCEHGxs0KpoTbljJ8Cl0/sendMessage?',json={"chat_id":-1001606089179,"text":'POST'})

        return HttpResponse('Get')
    elif request.method == 'POST':
        print('post')
        return HttpResponse('')