from ml_app.models import SaveAnalysis
from ml_app.serializer import SaveSerializer
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from user_profile_app.views import user_token
from .utils import twitter_analyzer
from django.contrib.auth.models import User
from user_profile_app.serializers import *

import json

# @user_token


@api_view(['POST', 'GET'])
def twitter_analysis(request):
    type = request.GET['type']
    try:
        if type == 'analysis':
            query = request.data['query']
            data, stats = twitter_analyzer(query)
            return JsonResponse({'data': data, 'stats': stats, 'success':True})

        elif type == 'classification':
            query = request.data['query']
            data, stats = twitter_analyzer(query)

            return JsonResponse({'data': data, 'stats': stats, 'success':True})
        else:
            return JsonResponse({'message': "The query must be most tweeted in real world...! min of 100 tweets", 'success':False})
    except:
        return JsonResponse({'message': "The query must be most tweeted in real world...! min of 100 tweets", 'success':False})


@api_view(['POST', 'GET', 'DELETE'])
def saved(request):
    # try:
    if request.method == 'POST':
        types = request.GET['type']
        if types == 'save-item':
            # user = json.loads(request.data['user'])
            username = request.data['user']['data']['user']
            user_data = User.objects.get(username=username)
            tweet_comment = request.data['data']['data']
            print(request.data['description'])
            tweet_id = request.data['data']['stats']['tweets']
            for i, j in zip(tweet_comment, tweet_id):
                i['comment'] = j

            data_saved = SaveAnalysis.objects.create(
                user=user_data, saved_data=tweet_comment, summary=request.data['description'], saved_query=request.data['query'])
            data_saved.save()
            serializer = SaveSerializer(data_saved)
            return JsonResponse({'message': 'Successfully saved the data to the database!','success':True})

        if types=='delete':
            user = json.loads(request.data['user'])
            username = user['data']['user']
            delete_save = SaveAnalysis.objects.filter(id=request.data['id'], user=User.objects.get(username=username).id)
            delete_save.delete()
            return JsonResponse({'message':'Successfully deleted the analysis..!', 'success':True})

    if request.method == 'GET':
        types = request.GET['type']
        if types == 'save':
            data = request.GET['user']
            username = data
            user = User.objects.get(username=username)
            obj = SaveAnalysis.objects.filter(user=user)
            serializer = SaveSerializer(obj, many=True)
            return JsonResponse({'data': serializer.data, 'success':True})

    # except:
    #     return JsonResponse({'message':"something went wrong!",'success':False})
