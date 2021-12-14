from django.contrib import admin
from .models import *

class GroupsAdmin(admin.ModelAdmin):
    list_display = ('name', 'tb')

class TimetableAdmin(admin.ModelAdmin):
    list_display = ('name', 'listgroups', 'link')

    def listgroups(self, obj):
        text = ''
        print(Groups.objects.filter(tb=obj).values('name'))
        print(obj)
        g = Groups.objects.filter(tb=obj).values('name')
        for g1 in g:
            text = text + g1.get('name') + ' '
        return text

class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'name')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'text', 'created')

# Register your models here.
admin.site.register(Groups, GroupsAdmin)
admin.site.register(Timetable, TimetableAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message, MessageAdmin)
