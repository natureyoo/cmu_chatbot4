from __future__ import print_function
from __future__ import unicode_literals

from django.shortcuts import render
from chat.models import *

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

@csrf_exempt
def startchat(request):
    
    '''
    Splash the main landing page (html file)
    '''
    return render(request, 'chats/chatting_screen.html', {})

@csrf_exempt
def query_to_engine(request):

    if request.method == 'POST':
        try:
            '''
            Send the request message to the engine
            '''

            '''
            Receive the return message from the engine
            '''

            pass
            #return HttpResponse('Successs!')

        except Exception as e:
            print(e)
            #return HttpResponse('Request was not in a POST type')

    pass