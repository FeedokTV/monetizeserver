from _sha1 import sha1
from datetime import date

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from pip._vendor.rich import json
from requests import request as req
import hashlib
from botpayment.models import Project, Ymbill

def payeer(request):
    return HttpResponse('1684240844')

@csrf_exempt
def yoomoneyNotification(request : WSGIRequest, user_id):


    # prjs = Project.objects.all()
    # for project in prjs:
    #     print(project.project_name)
    if Project.objects.filter(project_owner_id=user_id).exists():
        if request.method == 'GET':
            return HttpResponse('Тебе тут делать нечего')
        elif request.method == 'POST':
            # Calculating sha1 hash
            labelKey = str(request.POST['label']).replace('BPS', '').split('.')[0]
            projectId = str(request.POST['label']).replace('BPS', '').split('.')[1]
            print(labelKey)
            print(projectId)
            postStr = get_hash_check_string(request.POST, user_id)
            postStr = postStr.encode('utf-8')
            shaForTest = hashlib.sha1(postStr)

            print(deserializeYooMoneyConfig(user_id))

            secKey = deserializeSecretKey(projectId)['ym']
            r = req(method='POST',
                    url='https://api.telegram.org/bot5527748790:AAFdKl6ySucQ_FQWCEHGxs0KpoTbljJ8Cl0/sendMessage?',
                    json={"chat_id": user_id,
                          "text": str(secKey)})

            r = req(method='POST',
                    url='https://api.telegram.org/bot5527748790:AAFdKl6ySucQ_FQWCEHGxs0KpoTbljJ8Cl0/sendMessage?',
                    json={"chat_id": user_id,
                          "text": str(labelKey)})

            if request.POST['sha1_hash'] == shaForTest.hexdigest():
                if request.POST['operation_id'] == "test-notification":
                    r = req(method='POST', url='https://api.telegram.org/bot5527748790:AAFdKl6ySucQ_FQWCEHGxs0KpoTbljJ8Cl0/sendMessage?',json={"chat_id":user_id,"text":'Похоже вам пришёл проверочный платёж от YooMoney! Если это не вы то плохо'})
                    #r = req(method='POST', url='https://api.telegram.org/bot5527748790:AAFdKl6ySucQ_FQWCEHGxs0KpoTbljJ8Cl0/sendMessage?',json={"chat_id":ownerId,"text":str(deserializeYooMoneyConfig(id))})
                    return HttpResponse('Sucess')

                elif request.POST['operation_id'] != "" and request.POST['operation_id'] != "test-notification" and secKey == labelKey:
                    ymBill = Ymbill()
                    ymBill.bill_date = date.today()
                    ymBill.sender = request.POST['sender']
                    ymBill.withdraw = request.POST['amount']
                    ymBill.extra_info = request.POST['label']
                    ymBill.save()
                    r = req(method='POST',
                            url='https://api.telegram.org/bot5527748790:AAFdKl6ySucQ_FQWCEHGxs0KpoTbljJ8Cl0/sendMessage?',
                            json={"chat_id": user_id, "text": 'Пришёл платёж'})
                    return HttpResponse('Sucess payment')
                else:
                    return HttpResponse('failed :(')
            return HttpResponse(status=204)


def get_hash_check_string(postReq : dict, user_id : int):
    config = deserializeYooMoneyConfig(user_id)
    notificationSecret = config['secret']
    hashStr = postReq['notification_type'] + '&' + postReq['operation_id'] + '&' + postReq['amount'] + '&' + postReq['currency'] + '&' + postReq['datetime'] + '&' + postReq['sender'] + '&' + postReq['codepro'] + '&' + notificationSecret + '&' + postReq['label']
    return hashStr

def deserializeYooMoneyConfig(user_id : int):
    #pathToConfig = '/home/monetizeadmin/AdminBot/users/' + str(user_id) + '/paymentsConfig.json'
    pathToConfig = 'C:/Users/green/Desktop/AdminBot/users/' + str(user_id) + '/paymentsConfig.json'
    configJson = open(pathToConfig).read()  # opens the json file and saves the raw contents
    configData = json.loads(configJson)  # converts to a json structure
    return configData['yooMoney']

def deserializeSecretKey(id : int):
    #pathToConfig = '/home/monetizeadmin/AdminBot/projects/prjct_' + str(id) + '/secret_key.json'
    pathToConfig = 'C:/Users/green/Desktop/AdminBot/projects/prjct_' + str(id) + '/secret_key.json'
    secKeyJson = open(pathToConfig).read()  # opens the json file and saves the raw contents
    secKey = json.loads(secKeyJson)  # converts to a json structure
    return secKey