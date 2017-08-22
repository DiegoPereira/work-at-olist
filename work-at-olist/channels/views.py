from channels.models import Channel, Categories
from channels.serializers import ChannelSerializer, CategoriesSerializer
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.filter(id=0)
    serializer_class = CategoriesSerializer
    def get_queryset(self):
        queryset = []
        channel_name = self.request.query_params.get('channel', None)
        if channel_name is not None:
            if channel_name[-1] == "/":
                channel_name = channel_name[:-1]
            queryset = Categories.objects.all()
            channel = Channel.objects.get(name=channel_name)
            channel_id = channel.id
            queryset = queryset.filter(channel=channel_id)
        return queryset


class RelativesViewSet(APIView):
    def get(self, request):
        category_name = self.request.query_params.get('category', None)
        dict_response = {"relatives": [], "category": category_name}
        if category_name is not None:
            queryset = Categories.objects.filter(name=category_name)
            print (queryset)
            for category in queryset:
                ancestors = relatives_helper(category.get_ancestors())
                descendants = relatives_helper(category.get_descendants())
                dict_response["relatives"].append({"ancestors": ancestors, "descendants":descendants})

        return JsonResponse(dict_response)

def relatives_helper(category_list):
    categories_names = []
    for category in category_list:
        categories_names.append(category.name)
    return categories_names