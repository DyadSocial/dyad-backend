from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from. models import Chat, Message
from core.models import DyadUser 

# # Create your views here.


# def get_last_10_messages(chatId):
#     chat = get_object_or_404(Chat, id=chatId)
#     return chat.messages.order_by('-timestamp').all()[:10]

# def index(request):
#     return render(request, 'chat/index.html')

# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name': room_name
#     })

User = DyadUser()


# def get_last_10_messages(chatId):
#     chat = get_object_or_404(Chat, id=chatId)
#     return chat.messages.order_by('-timestamp').all()[:10]


# def get_user_contact(username):
#     user = get_object_or_404(User, username=username)
#     return get_object_or_404(Contact, user=user)


# def get_current_chat(chatId):
#     return get_object_or_404(Chat, id=chatId)


def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()

def get_user_object(username):
    print(f'{username}')
    return DyadUser.objects.filter(username = username)[0]

def get_chat_object(chatid):
    print(f'{chatid}')
    return Chat.objects.filter(chatid = chatid)[0]

def check_if_in_chatlog(username, chatlog):
    user = get_user_object(username)
    print(chatlog.participants.all())
    if user in chatlog.participants.all():
        print('the is already part of this chat')
    else:
        chatlog.participants.add(user)
        print('the user has been added to this chat')
    

def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, chatid = chatId)
    return chat.messages.order_by('-timestamp').all()[:10]

def make_new_chatlog(chatId, recipients):

    recipient_list = []

    for users in recipients:
        recipient_list.append(get_user_object(users))
    
    #create brand new chatlog
    new_chatlog = Chat.objects.create(chatid = data['roomname'])
    
    #add the 2 recipients to the chatlog, both users MUST EXIST already
    for add_users in recipient_list:
        new_chatlog.participants.add(add_users)
        new_chatlog.save()
    
    return new_chatlog









