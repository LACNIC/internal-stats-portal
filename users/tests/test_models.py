# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.contrib.auth import get_user_model


class UserTests(TestCase):
    def test_user_profile_auto_creation(self):
        """
        Testing if the user profile instance is created when an user is created
        """
        UserModel = get_user_model()
        user = UserModel(username='foo')
        user.save()
        self.assertTrue(user.userprofile is not None)

    def test_user_profile_creation(self):
        """
        User with user profile should be created succesfully
        """
        comment = "Comentario con acentuación."
        "El email es user@example.com"
        UserModel = get_user_model()
        user = UserModel(username='Américo')
        user.save()
        user.userprofile.comments = comment
        user.userprofile.save()
        self.assertEqual(user.userprofile.comments, comment)
