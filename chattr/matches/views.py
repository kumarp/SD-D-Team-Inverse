from models import RoomUsers
from chattr.interests.models import UserInterestLink, Interest
from chattr.ratings.models import UserRating
from chattr.jqchat.models import Room
from django.http import HttpResponse, HttpResponseRedirect
import datetime


# Matching conditionals - return reference to room
# Match any: Maximal non-zero shared interest count
def is_any(request):
    return '/room/any'

# Match all: All interests shared
def is_all(request):
    return '/room/all'

# Match randomly: Disregard interests
def is_random(request):
    return '/room/random'


# Perform matching, redirect
def match(request, is_match):
    
    # Get list of rooms waiting for a second user
    # Conditions:
    #    Only one user AND
    #    Last checked for messages < 5 seconds ago
    
    
    # Find all that meet requirements (all or maximal non-zero shared interest count)
    # Sort by rating, descending
    
    
    
    # If match found
    if(True):
        # Fill room with second user
        pass
    else:
        # Create new room, add user to it
        pass
    
    
    return HttpResponseRedirect(is_match(request))


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