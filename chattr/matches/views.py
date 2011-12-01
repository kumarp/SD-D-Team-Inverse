from models import RoomUsers
from django.contrib.auth.models import User
from chattr.interests.models import UserInterestLink, Interest
from chattr.ratings.models import UserRating
from chattr.jqchat.models import Room

from django.http import HttpResponse, HttpResponseRedirect
import datetime
import random


# Matching conditionals - return reference to room
# Match any: Maximal non-zero shared interest count
def is_any(request, set):
    return False

# Match all: All interests shared
def is_all(request, set):
    return False

# Match randomly: Disregard interests
def is_random(request, set):
    if len(set) == 0:
        return None
    return random.choice(set)


# Perform matching, redirect
def match(request, get_match):
    
    # Get list of rooms waiting for a second user
    # Conditions:
    #    Only one user AND
    #    Expired == False
    
    # TODO: Sort by rating, descending
    #.orderby('-user1.rating')   -- DOESN'T WORK, NEEDS USER RATING TABLE JOIN!
    waitingset = RoomUsers.objects.filter(user2 = None, expired = False)
    
    # Find all that meet requirements (all or maximal non-zero shared interest count)
    match = get_match(request, waitingset)
    
    # If match found
    if(match):
        # Fill room with second user
        match.user2 = request.user
        match.save()
        
        # :: Update room with matched properties
        
        # Room name used as status message
        match.room.name = 'INTERESTS HERE' # needs to be updated
        
        # TODO: Send action: Joined room
        
    else:
        # Create new room
        newroom = Room(name = 'Waiting for a second user... please be patient!', description_modified = 0)
        newroom.save()
        
        # Add user to it : RoomUsers entry with only first user
        match = RoomUsers(room = newroom, user1 = request.user)
        match.save()
        
        # TODO: Send action: Waiting for partner
        
        
    
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
