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

# class Influx_create(APIView):
#     def post(self):
#         json_body = self.request.POST
#         print(json_body)
#
#         client = InfluxDBClient('walter.smarthomy.com', 8086, 'admin', 'admin', 'MQTT_SMARTHOMY')
#         client.write_points(json_body)
#
#         consulta = 'select id,level,title,type,topic,value from homy order by time limit 10;'
#         result = client.query(consulta)
#         return Response(list(result))
#
# influx_create = Influx_create.as_view()