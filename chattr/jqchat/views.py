from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.html import escape

from models import Room, Message, messageManager
from chattr.matches.models import RoomUsers
from chattr.ratings.models import UserRating
from django.contrib.auth.models import User

import time

# The format of the date displayed in the chat window can be customised.
try:
    DATE_FORMAT = settings.JQCHAT_DATE_FORMAT
except:
    # Use default format.
    DATE_FORMAT = "H:i:s"

# How many messages to retrieve at most.
JQCHAT_DISPLAY_COUNT = getattr(settings, 'JQCHAT_DISPLAY_COUNT', 100) 

#------------------------------------------------------------------------------
@login_required
def window(request, id):
    """A basic chat client window."""

    ThisRoom = get_object_or_404(Room, id=id)

    return render_to_response('jqchat/chat_test.html', {'room': ThisRoom},
                              context_instance=RequestContext(request))

#------------------------------------------------------------------------------
@login_required
def WindowWithDescription(request, id):
    """A variant of the basic chat window, includes an updatable description to demonstrate
    how to extend the chat system."""

    ThisRoom = get_object_or_404(Room, id=id)

    return render_to_response('jqchat/chat_test_with_desc.html', {'room': ThisRoom},
                              context_instance=RequestContext(request))

#------------------------------------------------------------------------------                      
def end_chat(request, id):
    currentUser = User.objects.get(username = request.user)
    ThisRoom = get_object_or_404(Room, id=id)
    matchLink = RoomUsers.objects.get(room = ThisRoom)
    
    # Mark room as expired
    matchLink.expired = True
    matchLink.save()
    
    # Send "user has left chat" message
    messageManager.create_event(messageManager(), user = request.user, room = matchLink.room, event_id = 3)
    
    # Redirect
    if currentUser.email == "bogus@email.com":
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/interests/")
#------------------------------------------------------------------------------
class Ajax(object):
    """Connections from the jQuery chat client come here.

    We receive here 2 types of calls:
    - requests for any new messages.
    - posting new user messages.

    Any new messages are always returned (even if/when posting new data).

    Requests for new messages should be sent as a GET with as arguments:
    - current UNIX system time on the server. This is used so that the server which messages have
    already been received by the client.
    On the first call, this should be set to 0, thereafter the server will supply a new system time
    on each call.
    - the room ID number.
    
    Requests that include new data for the server (e.g. new messages) should be sent as a POST and 
    contain the following extra args:
    - an action code, a short string describing the type of data sent.
    - message, a string containing the message sent by the user.

    The returned data contains a status flag:
     1: got new data.
     2: no new data, nothing to update.

    This code is written as a class, the idea being that implementations of a chat window will 
    have extra features, so these will be coded as derived classes.
    Included below is a basic example for updating the room's description field.

    """

    # Note that login_required decorators cannot be attached here if the __call__ is to be overridden.
    # Instead they have to be attached to child classes.
    def __call__(self, request, id):

        if not request.user.is_authenticated():
            return HttpResponseBadRequest('You need to be logged in to access the chat system.')
    
        StatusCode = 0 # Default status code is 0 i.e. no new data.
        self.request = request
        try:
            self.request_time = float(self.request.REQUEST['time'])
        except:
            return HttpResponseBadRequest("What's the time?")
        self.ThisRoom = Room.objects.get(id=id)
        NewDescription = None

        if self.request.method == "POST":
            # User has sent new data.
            action = self.request.POST['action']
    
            if action == 'postmsg':
                # User is sending a message
                msg_text = self.request.POST['message']
    
                if len(msg_text.strip()) > 0: # Ignore empty strings.
                    Message.objects.create_message(self.request.user, self.ThisRoom, escape(msg_text))     

            if action == 'rate':
                # User is rating their partner
                rating_val = int(self.request.POST['rating'])
                roomLink = RoomUsers.objects.get(room = self.ThisRoom)
                currentuser = User.objects.get(username = self.request.user)
                
                # Determine which user in the roomLink is the partner
                if roomLink.user1 == currentuser:
                    partner = roomLink.user2
                else:
                    partner = roomLink.user1
                    
                # Get or create the UserRating link
                try:
                    curr = partner.get_profile()
                except:
                    curr = UserRating(user = partner, numRatings = 1, totalRating = 5, avgRating = 5)
                    
                # Increment number of ratings, add rating to total, re-calculate average
                curr.numRatings += 1
                curr.totalRating += rating_val
                curr.avgRating = float(curr.totalRating) / float(curr.numRatings)
                curr.save()
                
        else:
            # If a GET, make sure that no action was specified.
            if self.request.GET.get('action', None):
                return HttpResponseBadRequest('Need to POST if you want to send data.')

        # If using Pinax we can get the user's timezone.
        try:
            user_tz = self.request.user.account_set.all()[0].timezone
        except:
            user_tz = settings.TIME_ZONE
    
        # Extra JSON string to be spliced into the response.
        CustomPayload = self.ExtraHandling()
        if CustomPayload:
            StatusCode = 1
    
        # Get new messages - do this last in case the ExtraHandling has itself generated
        # new messages. 
        NewMessages = self.ThisRoom.message_set.filter(unix_timestamp__gt=self.request_time)
        if NewMessages:
            StatusCode = 1

        # Only keep the last X messages.
        l = len(NewMessages)
        if l > JQCHAT_DISPLAY_COUNT:
            NewMessages = NewMessages[l-JQCHAT_DISPLAY_COUNT:]
            
        response =  render_to_response('jqchat/chat_payload.json',
                                       {'current_unix_timestamp': time.time(),
                                        'NewMessages': NewMessages,
                                        'StatusCode': StatusCode,
                                        'NewDescription': NewDescription,
                                        'user_tz': user_tz,
                                        'CustomPayload': CustomPayload,
                                        'TimeDisplayFormat': DATE_FORMAT
                                        },
                                       context_instance=RequestContext(self.request))
        response['Content-Type'] = 'text/plain; charset=utf-8'
        response['Cache-Control'] = 'no-cache'
        return response

    def ExtraHandling(self):
        """We might want to receive/send extra data in the Ajax calls.
        This function is there to be overriden in child classes.
        
        Basic usage is to generate the JSON that then gets spliced into the main JSON 
        response.
        
        """
        return None
        

BasicAjaxHandler = Ajax()


#------------------------------------------------------------------------------
class DescriptionAjax(Ajax):
    """Example of how to handle calls with extra data (in this case, a room
    description field).
    """

    def ExtraHandling(self):
        # Check if new description sent.
        if self.request.method == "POST":
            action = self.request.POST['action']
            if action == 'change_description':
                # Note that we escape descriptions as a protection against XSS.
                self.ThisRoom.description = escape(self.request.POST['description'])
                self.ThisRoom.save()
                Message.objects.create_event(self.request.user, self.ThisRoom, 1)
        # Is there a description more recent than the timestamp sent by the client?
        # If yes, return an extra field to be tagged on to the JSON returned to the client.
        if self.ThisRoom.description and self.ThisRoom.description_modified > self.request_time:
            return ',\n        "description": "%s"' % self.ThisRoom.description
        
        return None

WindowWithDescriptionAjaxHandler = DescriptionAjax()
