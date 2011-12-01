from interestforms import NewInterestForm, AddInterestForm, RemoveInterestForm
from models import UserInterestLink, Interest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime

#view for user to manage their interests
def interest_manage_view(request):

    #find current user's interests
    interestquery = UserInterestLink.objects.filter(user__exact=request.user)
    #go through interests to make sure nothing is displayed more than once

    #when a button has been pressed
    if request.method == 'POST':
    
        #if user is adding an existing interest
        if 'addinterest' in request.POST:
            #create the link and set it to the current user
            link = UserInterestLink(user=request.user)
            #render forms
            addinterestform = AddInterestForm(request.user, request.POST, instance=link)
            newinterestform = NewInterestForm()
            reminterestform = RemoveInterestForm(request.user)
            #check form contents are valid
            if addinterestform.is_valid():
                #create new interest link
                uilink = addinterestform.save(commit=False)
                #if user doesn't already have this interest, save interest link
                if UserInterestLink.objects.filter(user__exact=request.user, interest__exact=uilink.interest).count() == 0:
                    uilink.save()
                #refresh page
                return HttpResponseRedirect('/interests')
        
        #if user is creating a new interest
        elif 'newinterest' in request.POST:
            #render forms
            newinterestform = NewInterestForm(request.POST)
            addinterestform = AddInterestForm(request.user)
            reminterestform = RemoveInterestForm(request.user)
            #check form contents are valid
            if newinterestform.is_valid():
                #create new interest
                interest = newinterestform.save(commit=False)
                #if interest doesn't already exist, create interest and link user to it
                check = Interest.objects.filter(name__iexact=interest.name)
                if check.count() == 0:
                    interest.save()
                    UserInterestLink(user=request.user, interest=interest).save()
                #if interest already exists, and user doesn't already have it, create link to it
                elif UserInterestLink.objects.filter(user__exact=request.user, interest__name__iexact=interest.name).count() == 0:
                    #check = check[:1]
                    UserInterestLink(user=request.user, interest=check[0]).save();
                #refresh page
                return HttpResponseRedirect('/interests')
                
        #if user is removing an interest
        elif 'reminterest' in request.POST:
            #render forms
            reminterestform = RemoveInterestForm(request.user, request.POST)
            addinterestform = AddInterestForm(request.user)
            newinterestform = NewInterestForm()
            #check form contents are valid
            if reminterestform.is_valid():
                #get selected interest link and delete it
                link = reminterestform.cleaned_data['interest']
                link.delete()
                return HttpResponseRedirect('/interests')
                
    #if a button hasn't been pressed
    else:
        #render forms
        newinterestform = NewInterestForm()
        addinterestform = AddInterestForm(request.user)
        reminterestform = RemoveInterestForm(request.user)

    return render_to_response('interestpage.html', 
                              {'addinterestform': addinterestform,
                               'newinterestform': newinterestform,
                               'reminterestform': reminterestform,
                               'links': interestquery
                               },
                              context_instance=RequestContext(request))
