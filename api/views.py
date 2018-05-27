from django.shortcuts import render
from rest_framework.views import APIView, Response
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer
from rest_framework.request import Request
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from influxdb import InfluxDBClient
from django.http import JsonResponse
from django.core.mail import send_mail
import requests
import json

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer



class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class Influx_view(APIView):
    def get(self,request,format=None):
        #consulta = 'select id,level,title,type,topic,value from homy limit 10'
        #response = query(consulta)
        #return Response({'results':list(response)})

        consulta = 'select id,level,title,type,topic,value from homy order by time limit 10;'
        ##client = InfluxDBClient('walter.smarthomy.com', 8086, 'admin', 'admin', 'MQTT_SMARTHOMY')
        client = InfluxDBClient('walter.smarthomy.com', 8086, 'admin', 'admin', 'HdF')
        result = client.query(consulta)
        return Response(list(result))
        ##return JsonResponse({'result': list(result)})


influx_rest = Influx_view.as_view()

class EmailNotification(APIView):
    def post(self,request,format=None):
        #print(request.data)
        remote_id = request.data['remote_id']
        email_to = request.data['email_to']
        subject = request.data['subject']
        message = request.data['message']
        language = request.data['language']
        #print(remote_id,email_to,subject,message,language)


        url = "http://cloud.smarthomy.com:8080/api/v1/hardware/bytag/" + remote_id
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImM2NGUyN2QyODRhYTk0MzFkZjRiMjg2ZGQ0ZWI2Y2JmMTBjYTljMWNlYTg0NTc5ZDVhMjFmZjRmNjRlOWEzZmI5Y2E0ZjgyYjFiZTVmZDliIn0.eyJhdWQiOiIxMSIsImp0aSI6ImM2NGUyN2QyODRhYTk0MzFkZjRiMjg2ZGQ0ZWI2Y2JmMTBjYTljMWNlYTg0NTc5ZDVhMjFmZjRmNjRlOWEzZmI5Y2E0ZjgyYjFiZTVmZDliIiwiaWF0IjoxNTI0MDk1ODY2LCJuYmYiOjE1MjQwOTU4NjYsImV4cCI6MTU1NTYzMTg2Niwic3ViIjoiNCIsInNjb3BlcyI6W119.CGw0bV0xCvx07H3LXnvFjPcn2s59Hfyoq4PXojV_KGJ-TtOfVK0I_SgA9WBxpy_133qxtYYo0VHgGziMaAv1sjKFKSSKA4HijhsDGFw3OB8p1G7XaUSz4DxQKcf9xmBM3dfiomSSJdd2WvBq8Zt_5Cry_b53dQ_vJ1ERqLQK95ef-X7LISANUKh6-M7sGKPdbHYaCEhIiUvufnOf6AxNkwtuA9pRI0sG6FHyoMvBgQtXr-uo0lgW1GKw9mkwLr9posRvG7S_CHvb4yJXQMrOOH-ig8wuDdgUWzMO3ZrWzDN75X3bMyFiiktPvaVhcuuiPDjUua9gkhhKR5loUXPXTtXM53-KYFYuwT645p2eCIiYxdetZCIfheimjUY-MHov7pTdssNlnf9IRLvX4FRg7yOWvRqViFUTt6-vN9x4PS5WPyuk_MzEWg0YzHHx9AxSC-FGBhQGcY3MMK75z3D_hDgxw9tmQ8HYlpwBXGImzxZkvmjgl0usmDp_UWMsKv4pgUvIxMBOHIUIIzjeAifosfEGjoZ74pvcdHd2DBeuCyHW3kYnomD5CGAMTlQ9IwIgcPmk9_GjIGPvvNo_itXjsJReWscp38JPMEW1dUO11O2_Rccih2AwFS6-StEarWmwDqFv4y8QBxwNy_JOYdyqmo8lgdx2Ufx0WChMHlxhjb0"

        response = requests.request("GET", url, headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})

        json_data = json.loads(response.text)
        #print(json_data)
        estado = json_data['status_label']['name']
        if (estado == 'Enabled'):
            send_mail(
                subject,
                message,
                'juan@smarthomy.com',
                [email_to],
                fail_silently=False,
            )
            return Response({'message':'Ok, email enviado'})
        else:
            return Response({'message': 'El hub no está habilitado '})

email_notif = EmailNotification.as_view()