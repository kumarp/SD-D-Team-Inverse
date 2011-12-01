from models import RoomUsers
from django.contrib.auth.models import User
from chattr.interests.models import UserInterestLink, Interest
from chattr.ratings.models import UserRating
from chattr.jqchat.models import Room, Message, messageManager

from django.http import HttpResponse, HttpResponseRedirect
import datetime
import random


# :: Matching handlers - return reference to specific room

# Match any: As many common interests as possible
def is_any(request, choices):
    # Don't include match_all rooms
    choices = choices.filter(matchAll = False)
    
    # Get user2's interests
    u2interests = [uil.interest for uil in UserInterestLink.objects.filter(user = request.user)]
    
    # Loop through user1 on each RoomUser in choices
    # Find RoomUsers with highest number of common interests
    maxcommon = 0
    match = None
    for ru in choices:
        # Get user1's interests
        u1interests = [uil.interest for uil in UserInterestLink.objects.filter(user = ru.user1)]
        
        # Find how many interests they have in common
        numcommon = 0
        for u1i in u1interests:
            if u1i in u2interests:
                numcommon += 1
        
        # If new max, keep
        if maxcommon < numcommon:
            match = ru
            maxcommon = 1
    
    # Return result or None if not found
    return match

# Match all: All interests shared
def is_all(request, choices):
    
    # Get user2's interests
    u2interests = [uil.interest for uil in UserInterestLink.objects.filter(user = request.user)]
    
    # Loop through user1 on each RoomUser in choices
    for ru in choices:
        # Get user1's interests
        u1interests = [uil.interest for uil in UserInterestLink.objects.filter(user = ru.user1)]
        
        # Check if user1 has all of user2's interests
        for u1i in u1interests:
            if u1i not in u2interests:
                continue
        
        # TODO: Check if user2 has all of user1's interests
        for u2i in u2interests:
            if u1i not in u1interests:
                continue
        
        # Simpler test? Didn't seem to work
        #if set(u1interests) == set(u2interests):
        
        # Interests match
        return ru
        
    # No match found
    return None

# Match randomly: Disregard interests unless 
def is_random(request, choices):
    
    # Don't include match_all rooms
    choices = choices.filter(matchAll = False)
    
    # Don't include match_any rooms
    choices = choices.filter(matchAny = False)
    
    # Can't randomly select from emptyset
    if len(choices) == 0:
        return None
    
    # TODO: Don't include match_any unless there's a shared interest
    return random.choice(choices)


# Perform matching, redirect
def match(request, get_match):
    
    # Get list of rooms waiting for a second user
    # Conditions:
    #    Only one user AND
    #    Non-expired room
    #waitingset = RoomUsers.objects.filter(user2 = None, expired = False)
    waitingset = RoomUsers.objects.select_related().filter(user2 = None, expired = False)
    
    
    
    
    # TODO: Sort by rating, descending
    
    waitingset = waitingset.order_by('-user1__userrating__avgRating')
    
    # Uncomment following lines to check if ordering worked correctly:
    
    #for i in waitingset:
    #    print i.user1.username + " " + str(i.user1.get_profile().avgRating)
    
    
    
    
    
    # Find all that meet requirements (all or maximal non-zero shared interest count)
    match = get_match(request, waitingset)
    
    # If match found
    if match:
        # Fill room with second user
        match.user2 = request.user
        match.save()

#        # Get relevant interests list
#        roominterests = set([uil.interest.name for uil in UserInterestLink.objects.filter(user = request.user)] +
#                         [uil.interest.name for uil in UserInterestLink.objects.filter(user = match.user1)])
#        
#        # Set room name to be list of interests
#        # TODO: Make update for user1 somehow
#        match.room.name = 'Interests: ' +  ', '.join(roominterests)
        
        # Event: Joined room
        messageManager.create_event(messageManager(), user = request.user, room = match.room, event_id = 2)
        
    else:
        # Create new room
        newroom = Room(name = 'Waiting for a second user... please be patient!', description_modified = 0)
        newroom.save()
        
        # Add user to it : RoomUsers entry with only first user
        match = RoomUsers(room = newroom, user1 = request.user)
        
        # Flag room as match_all restricted
        if get_match == is_all:
            match.matchAll = True
            
        # Flag room as match_any restricted
        if get_match == is_any:
            match.matchAny = True
        
        match.save()
        
        # Event: Joined room
        messageManager.create_event(messageManager(), user = request.user, room = match.room, event_id = 2)
        
        # Message: Waiting for partner
        messageManager.create_message(messageManager(), user = request.user, room = match.room,
                                      msg = ': Waiting for a chat partner... please be patient!')
    
    # Message: Interests
    messageManager.create_message(messageManager(), user = request.user, room = match.room,
                                  msg = 'has interests: ' + ', '.join([uil.interest.name for uil in UserInterestLink.objects.filter(user = request.user)]))
    
    return HttpResponseRedirect('/room/' + str(match.room.id))


# Views for redirecting users to matching chats

# Match any subset of interests
def match_any(request):
    return match(request, is_any)

# Match on all user interests
def match_all(request):
    return match(request, is_all)

# Match randomly
def match_random(request):
    return match(request, is_random)
