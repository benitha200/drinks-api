from django.shortcuts import render
from .models import Drinks
from .serializers import DrinkSerialiser
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def drink_list(request,format=None):

    # get all the drinks
    # serialize them
    # return json

    if request.method == 'GET':
        drinks = Drinks.objects.all()
        serializer = DrinkSerialiser(drinks, many=True)
        # return JsonResponse({"drinks": serializer.data})
        return Response (serializer.data)

    if request.method == 'POST':
        serializer = DrinkSerialiser(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, id,format=None):
    
    try:
        drink = Drinks.objects.get(pk=id)
    except Drinks.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': 
        serializer = DrinkSerialiser(drink)
        return Response(serializer.data)
     

    elif request.method == 'PUT':
        serializer = DrinkSerialiser(drink, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        drink.delete()
        return Response(status.HTTP_204_NO_CONTENT)
