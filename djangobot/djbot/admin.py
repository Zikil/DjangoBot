from django.contrib import admin
from .models import *
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render

import telegram

TOKEN = '1033970790:AAHgVbhB3yDw38jC4CIiEoi6jzbP5k_h0HQ'
bot = telegram.Bot(TOKEN)

def send_mes_to_users(text, users):
    #text = text
    for u in users:
        bot.sendMessage(chat_id=u, text=text)
    #bot.sendMessage(chat_id=340394898, text=text)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'name')
    actions = ['send_mes']

    def send_mes(self, request, queryset):
        if 'apply' in request.POST:  
            mes_text = request.POST['text']
            users= []
            for u in queryset:
                users.append(u.external_id)
            print(users)
            send_mes_to_users(mes_text, users)
            self.message_user(request, "mes was be send")
            return HttpResponseRedirect(request.get_full_path())
        form = BroadcastForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        print(request.POST)
        return render(request, "admin/broadcast_message.html", {'items': queryset, 'form': form})


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


class MessageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'text', 'created')

# Register your models here.
admin.site.register(Groups, GroupsAdmin)
admin.site.register(Timetable, TimetableAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message, MessageAdmin)
