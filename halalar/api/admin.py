from django.contrib import admin

from .models import Profile, Message

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'age', 'gender', 'city', 'country',)
    list_filter = ('age', 'gender', 'city', 'country',)
    search_fields = ('user__username', 'user__email', 'token', 'religion', 'family', 'selfx', 'community', 'career',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp', 'body',)
    list_filter = ('timestamp',)
    search_fields = ('sender__user__username', 'recipient__user__username', 'body',)