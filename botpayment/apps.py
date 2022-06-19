from django.apps import AppConfig


class BotpaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'botpayment'

    def ready(self):
        from botpayment.models import Projects
        from django.urls import path
        from monetizeserver.urls import urlpatterns
        from botpayment.views import index
        allProjects = Projects.objects.all()
        for prj in allProjects:
            print(prj.project_id)
            urlpatterns.append(path('prj_' + str(prj.project_id), index))

