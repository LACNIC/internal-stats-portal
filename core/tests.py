# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError, DataError
from django.forms import ValidationError
from django.utils import timezone
from .models import DataSource, Database, Tag
from .forms import publication_model_form_factory


class DataSourceTests(TestCase):
    def test_datasource_model_empty(self):
        datasource = DataSource.objects.create(notes='test')
        datasource.clean_fields()

    def test_datasource_unique_constraint(self):
        """
        Should not allow two datasources with the same notes
        """
        with self.assertRaises(IntegrityError):
            notes = 'Esto es una nota con acentuación.'
            DataSource.objects.create(notes=notes)
            DataSource.objects.create(notes=notes)


class DatabaseTests(TestCase):
    def test_database_model_empty(self):
        with self.assertRaises(ValidationError):
            database = Database.objects.create()
            database.clean_fields()

    def test_database_unique_constraint(self):
        """
        Should not allow two databases with the same name
        """
        with self.assertRaises(IntegrityError):
            name = 'Servidor nro. 1 de LACNIC.'
            Database.objects.create(name=name)
            Database.objects.create(name=name)

    def test_database_name_length(self):
        """
        Should not allow a database with a name length longer than
        100 characters
        """
        with self.assertRaises(DataError):
            name = 'a' * 101
            database = Database(name=name)
            database.save()


class TagTests(TestCase):
    def test_tag_model_empty(self):
        with self.assertRaises(ValidationError):
            tag = Tag.objects.create()
            tag.clean_fields()

    def test_tag_unique_constraint(self):
        """
        Should not allow two tags with the same name
        """
        with self.assertRaises(IntegrityError):
            name = 'This tag is a test'
            Tag.objects.create(name=name)
            Tag.objects.create(name=name)

    def test_tag_name_length(self):
        """
        Should not allow a tag with a name length longer than 100 characters
        """
        with self.assertRaises(DataError):
            name = 'a' * 101
            tag = Tag(name=name)
            tag.save()


class PublicationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        UserModel = get_user_model()
        cls.superuser = UserModel(username='superuser 1', is_staff=True,
                                  is_superuser=True)
        cls.superuser.save()
        cls.user_1 = UserModel(username='user 1', is_staff=True,
                               is_superuser=False)
        cls.user_2 = UserModel(username='user 2', is_staff=True,
                               is_superuser=False)
        cls.user_1.save()
        cls.user_2.save()
        cls.datasource_1 = DataSource.objects.create(notes='This is a note.')
        cls.datasource_2 = DataSource.objects.create(notes="This isn't a note.")
        cls.database_1 = Database.objects.create(name='MySQL db at LACNIC')
        cls.database_2 = Database.objects.create(name='Postgre db at Amazon')
        cls.tag_1 = Tag.objects.create(name='Test are important')
        cls.tag_2 = Tag.objects.create(name='Quality assurance')
        cls.programming_language_1 = 'ada'
        cls.programming_language_2 = 'go'
        cls.programming_language_3 = 'fortran'
        cls.programming_language_4 = 'erlang'

    def test_publication_model_empty(self):
        data = {}
        form = publication_model_form_factory(self.superuser)(data)
        self.assertFalse(form.is_valid())

    def test_publication_model_minimal_required_fields(self):
        data = {
            'name': 'Publication name',
            'creator': self.superuser.pk,
            'responsibles': [self.user_1.pk, self.user_2, ],
            'file_path': 'home/user/desktop/',
            'created': timezone.now(),
            'modified': timezone.now() + datetime.timedelta(days=1),
            'tags': [self.tag_1, ],
        }
        form = publication_model_form_factory(self.superuser)(data)
        self.assertTrue(form.is_valid())

    def test_publication_model_all_fields_filled(self):
        data = {
            'name': 'Publication name',
            'description': 'This is a description',
            'programming_language': self.programming_language_1,
            'update_value': 10,
            'update_type': 'mins',
            'creator': self.superuser.pk,
            'responsibles': [self.user_1.pk, self.user_2],
            'server_path': 'http://192.168.1.1/example/',
            'file_path': 'home/user/desktop/',
            'publishable': True,
            'created': timezone.now(),
            'modified': timezone.now() + datetime.timedelta(days=1),
            'tags': [self.tag_1, ],
        }
        form = publication_model_form_factory(self.superuser)(data)
        self.assertTrue(form.is_valid())

    def test_publication_model_update_field_constraint(self):
        data = {
            'name': 'Publication name',
            'creator': self.superuser,
            'file_path': 'home/user/desktop/',
            'update_type': 'mins',
            'created': timezone.now(),
            'modified': timezone.now() + datetime.timedelta(days=1)
        }
        form = publication_model_form_factory(self.superuser)(data)
        self.assertFalse(form.is_valid())

    def test_publication_creation_superuser(self):
        data = {
            'name': 'Publication name',
            'creator': self.superuser.pk,
            'responsibles': [self.user_1.pk, self.user_2, ],
            'file_path': 'home/user/desktop/',
            'created': timezone.now(),
            'modified': timezone.now() + datetime.timedelta(days=1),
            'tags': [self.tag_1, ],
        }
        form = publication_model_form_factory(self.superuser)(data)
        self.assertTrue(form.is_valid())

    def test_publication_creation_normal_user(self):
        data = {
            'name': 'Publication name',
            'creator': self.user_1.pk,
            'responsibles': [self.user_1.pk, self.user_2, ],
            'file_path': 'home/user/desktop/',
            'created': timezone.now(),
            'modified': timezone.now() + datetime.timedelta(days=1),
            'tags': [self.tag_1, ],
        }
        form = publication_model_form_factory(self.superuser)(data)
        self.assertTrue(form.is_valid())

    def test_publication_update_constraint(self):
        data = {
            'name': 'Publication constraint',
            'responsibles': [self.user_1.pk, self.user_2, ],
            'file_path': 'home/user/desktop/',
            'publishable': True,
            'created': timezone.now(),
            'modified': timezone.now() + datetime.timedelta(days=1),
            'tags': [self.tag_1, ],
        }
        form = publication_model_form_factory(self.user_1)(data)
        self.assertTrue(form.is_valid())

        pub = form.save()
        data = {
            'pk': pub.pk,
            'name': 'Publication updated constraint',
            'responsibles': [self.user_1.pk, self.user_2, ],
            'file_path': 'home/user/desktop/',
            'created': timezone.now(),
            'modified': timezone.now() + datetime.timedelta(days=1),
            'tags': [self.tag_1, ],
        }
        form = publication_model_form_factory(self.user_2)(data, instance=pub)
        self.assertFalse(form.is_valid())
