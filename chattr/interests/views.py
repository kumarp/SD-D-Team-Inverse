from interestforms import NewInterestForm, AddInterestForm
from models import UserInterestLink, Interest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime

#view for user to manage their interests
def interest_manage_view(request):

    #find current user's interests
    query = UserInterestLink.objects.filter(user__exact=request.user)
    #go through interests to make sure nothing is displayed more than once
    links = []
    for item in query:
        if item.interest.name not in links:
            links.append(item.interest.name)

    #when a button has been pressed
    if request.method == 'POST':
    
        #if user is adding an existing interest
        if 'addinterest' in request.POST:
            #create the link and set it to the current user
            link = UserInterestLink(user=request.user)
            #render forms
            addinterestform = AddInterestForm(request.POST, instance=link)
            newinterestform = NewInterestForm()
            #check form contents are valid
            if addinterestform.is_valid():
                #save interest link
                addinterestform.save()
                #refresh page
                return HttpResponseRedirect('/interests')
        
        #if user is creating a new interest
        elif 'newinterest' in request.POST:
            #render forms
            newinterestform = NewInterestForm(request.POST)
            addinterestform = AddInterestForm()
            #check form contents are valid
            if newinterestform.is_valid():
                #save new interest
                interest = newinterestform.save()
                #create link to current user
                UserInterestLink(user=request.user, interest=interest).save()
                #refresh page
                return HttpResponseRedirect('/interests')
                
    #if a button hasn't been pressed
    else:
        #render forms
        newinterestform = NewInterestForm()
        addinterestform = AddInterestForm()

    return render_to_response('interestpage.html', {'addinterestform': addinterestform, 'newinterestform': newinterestform, 'links': links})
