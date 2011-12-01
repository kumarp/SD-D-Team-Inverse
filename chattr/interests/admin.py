from interests.models import Interest, UserInterestLink
from django.contrib import admin

# register the Interest and UserInterestLink tables
admin.site.register(Interest)
admin.site.register(UserInterestLink)