from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from. models import Chat, Message
from core.models import DyadUser 

"""
FILE AUTHOR: SAM
"""

User = DyadUser()



def index(request):
    """
    renders a base HTML webpage for entering a chat room
    FOR TESTING PURPOSES ONLY, NOT PART OF THE MAIN DYAD PROGRAM
    """
    return render(request, 'chat/index.html')

def room(request, room_name):
    """
    renders a webpage for testing the websocket
    FOR TESTING PURPOSES ONLY, NOT PART OF THE MAIN DYAD PROGRAM
    """
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

def get_user_object(username):
    """
    retrieves and returns the last 10 messages of a chat object by the latest message objects
    """  
    print(f'{username}')
    return DyadUser.objects.filter(username = username)[0]

def get_chat_object(chatid):
    """
    retrieves and returns an entire chat object
    """
    print(f'{chatid}')
    return Chat.objects.filter(chatid = chatid)[0]

def check_if_in_chatlog(username, chatlog):
    """
    checks if a user exist in a chatlog or not, adds them to a chatlog if they do not
    exist in there
    """
    user = get_user_object(username)
    print(chatlog.participants.all())
    if user in chatlog.participants.all():
        print('the is already part of this chat')
    else:
        chatlog.participants.add(user)
        print('the user has been added to this chat')
    

def get_last_10_messages(chatId):
    """
    retrieves and returns the last 10 messages of a chat object by the latest message objects
    """    
    chat = get_object_or_404(Chat, chatid = chatId)
    return chat.messages.order_by('-timestamp').all()[:10]

def make_new_chatlog(chatId, recipients):
    """
    Makes a brand new chatlog with a recipients list, this function is called in the event
    of a new websocket being created that has the name of a chatlog that is not in the database
    """
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









