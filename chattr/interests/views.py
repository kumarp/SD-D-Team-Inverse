from interestforms import NewInterestForm, AddInterestForm, RemoveInterestForm
from models import UserInterestLink, Interest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime

# View for user to manage their interests
def interest_manage_view(request):

    # Find current user's interests
    interestquery = UserInterestLink.objects.filter(user__exact=request.user)
    # Go through interests to make sure nothing is displayed more than once

    # When a button has been pressed
    if request.method == 'POST':
    
        # If user is adding an existing interest
        if 'addinterest' in request.POST:
            # Create the link and set it to the current user
            link = UserInterestLink(user=request.user)
            # Render forms
            addinterestform = AddInterestForm(request.user, request.POST, instance=link)
            newinterestform = NewInterestForm()
            reminterestform = RemoveInterestForm(request.user)
            # Check form contents are valid
            if addinterestform.is_valid():
                # Create new interest link
                uilink = addinterestform.save(commit=False)
                # If user doesn't already have this interest, save interest link
                if UserInterestLink.objects.filter(user__exact=request.user, interest__exact=uilink.interest).count() == 0:
                    uilink.save()
                # Refresh page
                return HttpResponseRedirect('/interests')
        
        # If user is creating a new interest
        elif 'newinterest' in request.POST:
            # Render forms
            newinterestform = NewInterestForm(request.POST)
            addinterestform = AddInterestForm(request.user)
            reminterestform = RemoveInterestForm(request.user)
            # Check form contents are valid
            if newinterestform.is_valid():
                # Create new interest
                interest = newinterestform.save(commit=False)
                # If interest doesn't already exist, create interest and link user to it
                check = Interest.objects.filter(name__iexact=interest.name)
                if check.count() == 0:
                    interest.save()
                    UserInterestLink(user=request.user, interest=interest).save()
                # If interest already exists, and user doesn't already have it, create link to it
                elif UserInterestLink.objects.filter(user__exact=request.user, interest__name__iexact=interest.name).count() == 0:
                    #check = check[:1]
                    UserInterestLink(user=request.user, interest=check[0]).save();
                # Refresh page
                return HttpResponseRedirect('/interests')
                
        # If user is removing an interest
        elif 'reminterest' in request.POST:
            # Render forms
            reminterestform = RemoveInterestForm(request.user, request.POST)
            addinterestform = AddInterestForm(request.user)
            newinterestform = NewInterestForm()
            # Check form contents are valid
            if reminterestform.is_valid():
                # Get selected interest link and delete it
                link = reminterestform.cleaned_data['interest']
                link.delete()
                return HttpResponseRedirect('/interests')
                
    # If a button hasn't been pressed
    else:
        # Render forms
        newinterestform = NewInterestForm()
        addinterestform = AddInterestForm(request.user)
        reminterestform = RemoveInterestForm(request.user)

    # Render view forms to interestpage.html template
    return render_to_response('interestpage.html', 
                              {'addinterestform': addinterestform,
                               'newinterestform': newinterestform,
                               'reminterestform': reminterestform,
                               'links': interestquery
                               },
                              context_instance=RequestContext(request))
