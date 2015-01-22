import json
from . import register_method
from utils import genhmac
from django.conf import settings
from django.contrib.auth.models import User
from django.conf.urls import patterns, url
from django.http import HttpResponse
from django.db.models import Q


def testview(request, param):
    data = {'status': 'ok'}
    jsondata = json.dumps(data)
    return HttpResponse(jsondata, content_type='application/json')


class PWD:
    DESCRIPTION = 'Register using user and password. '
    VALID_PIPELINES = ('check_whitelisted', 'check_blacklisted',
            'check_total_max')
    VALID_FIELDS = ('name', 'type', 'required', 'regex', 'min', 'max')
    CONFIG = {}
    PIPELINES = {
        "register-pipeline": [],
        "authenticate-pipeline": []
    }

    def authenticate_error(self):
        d = {'status': 'nok'}
        return d

    def authenticate(self, event, data):
        d = {'status': 'ok'}
        msg = data.get('username', '')
        if not msg:
            msg = data.get('email', '')

        pwd = data['password']

        try:
            u = User.objects.get(Q(username=msg)|Q(email=msg))
        except:
            return self.authenticate_error()

        if event != 0 and u.userdata.event != event:
            return self.authenticate_error()

        if not u.check_password(pwd):
            return self.authenticate_error()

        d['username'] = u.username
        d['auth-token'] = genhmac(settings.SHARED_SECRET, u.username)
        return d

    views = patterns('',
        url(r'^test/(\w+)$', testview),
    )


register_method('user-and-password', PWD)
