from _sha1 import sha1
from datetime import date

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
# Create your views here.
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from payeer.api import payeer_api
from payeer.constants import CURRENCY_USD
from pip._vendor.rich import json
from requests import request as req
import hashlib
from botpayment.models import Project, Ymbill

def payeer(request):
    return HttpResponse('1684240844')


@csrf_exempt
def api(request : WSGIRequest):
    if request.method == 'GET':
        return HttpResponse(content='Hello! Bye bye!', status=500)
    elif request.method == 'POST':
        if request.POST['action'] == 'YOOKASSA_PAYMENT_LINK':
            from yookassa import Configuration, Payment
            import uuid

            Configuration.account_id = request.POST['account_id']
            Configuration.secret_key = request.POST['secret_key']

            payment_link, id = generate_yookassa_url(float(request.POST['value']))

            return JsonResponse({"url": payment_link, "id": id})
        if request.POST['action'] == 'YOOKASSA_CHECK_PAYMENT':
            from yookassa import Configuration, Payment
            import uuid

            Configuration.account_id = request.POST['account_id']
            Configuration.secret_key = request.POST['secret_key']

            payment = Payment.find_one(payment_id=request.POST['payment_id'])

            if payment.status == 'succeeded':
                return JsonResponse({'is_payed':True})
            else:
                return JsonResponse({'is_payed': False})



@csrf_exempt
def yoomoneyNotification(request : WSGIRequest, user_id):

    # Check if we REALLY have this user
    if Project.objects.filter(project_owner_id=user_id).exists():
        # We dont need a get request here, so go away mr.intruder
        if request.method == 'GET':
            return HttpResponse(content='Hello! Bye bye!', status=500)
        elif request.method == 'POST':
            # Calculating sha1 hash

            # Get our hash (sending to func user_id to deserialize it)
            postStr = get_hash_check_string(request.POST, user_id)
            postStr = postStr.encode('utf-8')
            shaForTest = hashlib.sha1(postStr)

            # Check if hash is good!
            if request.POST['sha1_hash'] == shaForTest.hexdigest():
                # You're welcome, but...
                # Maybe its test notification?
                if request.POST['operation_id'] == "test-notification":
                    r = req(method='POST', url='https://api.telegram.org/bot5527748790:AAFdKl6ySucQ_FQWCEHGxs0KpoTbljJ8Cl0/sendMessage?',json={"chat_id":user_id,"text":'Похоже вам пришёл проверочный платёж от YooMoney! Если это не вы то плохо'})
                    return HttpResponse('Sucess')

                # Ok, thats not a test notification
                # We guess that its payments http notification
                # Working with a label, We want to know thats notif from our bot, not other such as money transfer

                labelKey = str(request.POST['label']).replace('BPS', '').split('.')[0]
                projectId = str(request.POST['label']).replace('BPS', '').split('.')[1]
                secKey = deserializeSecretKey(projectId)['ym']

                # Wow thats a good label!

                # Maybe its our notif from bot??
                if request.POST['operation_id'] != "" and request.POST['operation_id'] != "test-notification" and secKey == labelKey:
                    # Hooray! Its our notification
                    # Lets update our ymBills db
                    if not Ymbill.objects.filter(extra_info=user_id).exists(str(request.POST['label'])):
                        ymBill = Ymbill()
                        ymBill.bill_date = date.today()
                        ymBill.sender = request.POST['sender']
                        ymBill.withdraw = request.POST['amount']
                        ymBill.extra_info = request.POST['label']
                        ymBill.save()
                        return HttpResponse('Sucess payment')
                    else:
                        return HttpResponse('Are you a wizzard?!')
                    return HttpResponse('Sucess payment')
                else:
                    # Huh... No..
                    return HttpResponse('failed :(')
            else:
                return HttpResponse('Bad sha1')
    else:
        return HttpResponse(status=500,content='#*$(&^#&(@*#^>:(')


def generate_yookassa_url(value : float):
    from yookassa import Configuration, Payment
    import uuid

    Configuration.account_id = 924840
    Configuration.secret_key = 'test_LEwZqiKLC1FeVli7dKON9-5na5RtwGOya_u5OfwlF9s'

    payment = Payment.create({
        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://185.246.67.118/"
        },
        "capture": True,
        "description": "Bot order"
    }, uuid.uuid4())


    confirmation_url = payment.confirmation.__dict__['_ConfirmationRedirect__confirmation_url']
    payment_id = payment.id

    return confirmation_url,payment_id

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

def get_hash_check_string_payeer(postReq : dict):
    key = 'monetize'
    hashStr = postReq['m_operation_id'] + ':' + postReq['m_operation_ps'] + ':' + postReq['m_operation_date'] + ':' + postReq[
        'm_operation_pay_date'] + ':' + postReq['m_shop'] + ':' + postReq['m_orderid'] + ':' + postReq[
                  'm_amount'] + ':' + postReq['m_curr'] + ':' + postReq['m_desc'] + ':' + postReq['m_status'] + ':' + str(key)