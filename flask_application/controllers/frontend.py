#!/usr/bin/env python

import datetime

from flask import Blueprint
from flask.ext.security import login_required

from flask_application import app
from flask_application.controllers import TemplateView

frontend = Blueprint('frontend', __name__)


class IndexView(TemplateView):
    blueprint = frontend
    route = '/'
    template_name = 'home/index.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'now': datetime.datetime.now(),
            'config': app.config
        }


class BrowseView(TemplateView):
    blueprint = frontend
    route = '/browse'
    template_name = 'browse.html'

    def get_context_data(self, *args, **kwargs):
        return{
            'pics': 9
        }


class ProfileView(TemplateView):
    blueprint = frontend
    route = '/profile'
    template_name = 'profiles/profile.html'
    decorators = [login_required]

    def get_context_data(self, *args, **kwargs):
        return {
            'content': 'This is the profile page',
            'username': '<username>'
        }
