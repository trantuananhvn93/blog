from django.contrib import admin
from .models import Post, Comment


# class PostAdmin(admin.ModelAdmin):
#     list_display  = ('title', 'published', 'allow_comments')
#     list_filter   = ('published',)
#     search_fields = ('title', 'content')
#     fieldsets = ((None, 
#                   {'fields': ('title',  'content', 
#                               'allow_comments', 'published',)}),)

# admin.site.register(Post, PostAdmin)

admin.site.register(Post) 

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

