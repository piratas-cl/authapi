from django import forms
from django.contrib import admin
from api.models import AuthEvent, UserData, ACL
from authmethods.models import Message, ColorList, Code, Connection
from authmethods import METHODS

# Register your models here.

class AuthEventAdminForm(forms.ModelForm):
    class Meta:
        model = AuthEvent
        fields = ('name', 'auth_method', 'auth_method_config', 'metadata')
        choices = []
        for k in METHODS.keys():
            choices.append((k, k + ': ' + METHODS.get(k).DESCRIPTION))

        widgets = {
                'auth_method':
                forms.Select(attrs={'obj':'str'}, choices=choices),
        }

class AuthEventAdmin(admin.ModelAdmin):
    form = AuthEventAdminForm
    list_display = ('id', 'name', 'auth_method')


class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'status')


class ACLAdmin(admin.ModelAdmin):
    list_display = ('user', 'perm', 'object_type', 'object_id')
    list_filter = ('perm', 'object_type')


class ColorListAdmin(admin.ModelAdmin):
    pass


class MessageAdmin(admin.ModelAdmin):
    pass


class CodeAdmin(admin.ModelAdmin):
    pass


class ConnectionAdmin(admin.ModelAdmin):
    pass


admin.site.register(AuthEvent, AuthEventAdmin)
admin.site.register(UserData, UserDataAdmin)
admin.site.register(ACL, ACLAdmin)
admin.site.register(ColorList, ColorListAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(Connection, ConnectionAdmin)
