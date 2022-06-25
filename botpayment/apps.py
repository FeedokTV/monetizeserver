from django.apps import AppConfig
from asgiref.sync import sync_to_async


class BotpaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'botpayment'