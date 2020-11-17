# coding=utf-8
#
# Copyright © 2020 Quick Help For Meals, LLC. All rights reserved.
#
# This file is part of VeggieBook.
#
# VeggieBook is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the license only.
#
# VeggieBook is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or fitness for a particular purpose. See the
# GNU General Public License for more details.
#

import re

import httplib2
from oauth2client.crypt import AppIdentityError

__author__ = 'danieldipasquo'

import string
import random

from django.contrib.auth.models import User
from openid.consumer.consumer import SUCCESS
from oauth2client.client import verify_id_token
from qhmobile.models import UserProfile


class GoogleBackend:
    def authenticate(self, openid_response):
        if openid_response is None:
            return None
        if openid_response.status != SUCCESS:
            return None

        google_email = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.email')
        google_firstname = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.firstname')
        google_lastname = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.lastname')
        try:
            #user = User.objects.get(username=google_email)
            # Make sure that the e-mail is unique.
            user = User.objects.get(email=google_email)
            user.first_name = google_firstname
            user.last_name = google_lastname
            user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(google_email, google_email, self.id_generator())
            user.first_name = google_firstname
            user.last_name = google_lastname
            user.save()
            user = User.objects.get(username=google_email)
            return user

        return user

    def get_user(self, user_id):

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def id_generator(self, size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))


class GoogleTokenBackend:
    def get_user(self, user_id):

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def id_generator(self, size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    def authenticate(self, token):
        if token is None:
            return None

        try:
            response = verify_id_token(id_token=token, audience=None)
        except AppIdentityError as error:
            print error
            return None

        # verified without the audience above, but now we check a wildcard audience for all devices
        audience_in_response = response['aud']

        if not re.match(r'1080211826488.*\.apps\.googleusercontent\.com', audience_in_response):
            return None

        google_email = response['email']

        user = None

        try:
            #user = User.objects.get(username=google_email)
            # Make sure that the e-mail is unique.
            user = User.objects.get(email=google_email)
            user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(google_email, google_email, self.id_generator())
            user.save()
            user = User.objects.get(username=google_email)
            return user

        return user


class DeviceIdBackend:
    """
    Authentication by Device ID only associates a user with their device ID. If a user is created this way, they will
    not have an email or password and their username will have been randomly generated.
    """
    def get_user(self, user_id):
        """Get the user ID for a user that authenticates with a device ID.

        :param user_id: the user ID for the user
        :return: the user associated with the provided user ID if one exists, `None` otherwise
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, device_id=None):
        """Authenticate a user with their device ID.

        :param device_id: a device ID for a user
        :return: a user if authentication succeeded, `None` otherwise
        """
        if device_id is None:
            return None

        try:
            user_profile = UserProfile.objects.get(deviceId=device_id)
            return user_profile.user
        except UserProfile.DoesNotExist:
            return None
