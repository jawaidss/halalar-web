from django.contrib import admin

from .models import Profile, Message

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'city', 'country',)
    list_filter = ('age', 'gender', 'city', 'country',)
    search_fields = ('user__username', 'user__email', 'religion', 'family', 'selfx', 'community', 'career',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp', 'body',)
    list_filter = ('timestamp',)
    search_fields = ('sender__username', 'recipient__username', 'body',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message, MessageAdmin)