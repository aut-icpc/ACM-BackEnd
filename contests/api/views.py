from django.shortcuts import render
from django.http import JsonResponse
from ..models import ACM
from ..api import serializers
from rest_framework.generics import ListAPIView,RetrieveAPIView

# def ACMAPI(request):
#     contest = ACM.objects.all()
#     return JsonResponse(serializers.ACMSerializer(contest, many = True).data, safe = False)
      
      
#         # return JsonResponse(MovieSerializer(movies, many=True).data, safe=False)


class ACMTitleistView(ListAPIView):
    queryset = ACM.objects.all()
    serializer_class = serializers.ACMTitleSerializer


class ACMRetriveView(RetrieveAPIView):
    queryset = ACM.objects.all()
    serializer_class = serializers.ACMSerializer
