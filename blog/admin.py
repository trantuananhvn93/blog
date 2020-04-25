from django.contrib import admin
from .models import Tutorial
from django.db import models
from pagedown.widgets import AdminPagedownWidget

# class TutorialAdmin(admin.ModelAdmin):

#     fieldsets = [
#         ("Title/date", {'fields': ["tutorial_title", "tutorial_published"]}),
#         ("Content", {"fields": ["tutorial_content"]})
#     ]

#     formfield_overrides = {
#         models.TextField: {'widget': AdminPagedownWidget},
#         }


admin.site.register(Tutorial) #,TutorialAdmin)



