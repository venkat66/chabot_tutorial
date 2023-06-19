import random
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from chatbot_tutorial.models import *


def login_view(request):
    if request.method == 'POST':
        # Attempt to sign user in
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("chat")
        else:
            messages.error(request, 'Invalid username and/or password.')
            return redirect('login')
    return render(request, 'chatbot_tutorial/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = email
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            return redirect('register')
         # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except:
            messages.error(request, "Account already exist's with this email.")
            return redirect('register')
        login(request, user)
        return redirect('chat')
        

    return render(request, 'chatbot_tutorial/register.html')

@login_required(login_url='login')
def calls_data(request):
    context ={}
    data = ChatRecordsModel.objects.all()
    context['data'] = data
    return render(request, 'chatbot_tutorial/calls-data.html',context)

@login_required(login_url='login')
def chat(request):
    context = {}
    return render(request, 'chatbot_tutorial/chatbot.html', context)
    # return render(request, 'chatbot_tutorial/test.html', context)


def respond_to_websockets(message):
    jokes = {
     'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
     'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
     'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] 
     }  

    result_message = {
        'type': 'text'
    }
    email = message['user']
    user = User.objects.get(username=email)
    chat_record, created= ChatRecordsModel.objects.get_or_create(user=user)
    if 'fat' in message['text']:
        result_message['text'] = random.choice(jokes['fat'])
        chat_record.fat_count+=1
    
    elif 'stupid' in message['text']:
        result_message['text'] = random.choice(jokes['stupid'])
        chat_record.stupid_count+=1
    
    elif 'dumb' in message['text']:
        result_message['text'] = random.choice(jokes['dumb'])
        chat_record.dumb_count+=1

    elif message['text'] in ['hi', 'hey', 'hello']:
        result_message['text'] = "Hello to you too! If you're interested in yo mama jokes, just tell me fat, stupid or dumb and i'll tell you an appropriate joke."
    else:
        result_message['text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."
    chat_record.save()
    return result_message
    