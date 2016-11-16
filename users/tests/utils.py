from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class FixtureTestCase(APITestCase):
    fixtures = ('initial_data.json',)

    superuser_data = {'id': 17, 'username': 'superuser', 'first_name': 'super',
                      'last_name': 'user', 'email': ''}

    @classmethod
    def setUpTestData(cls):
        pass
        # UserModel = get_user_model()
        # # Staff group creation
        # staff_group = Group.objects.create(name='staff')
        # # Add user permission
        # ct = ContentType.objects.get_for_model(UserModel)
        # permission = Permission.objects.get(codename='add_datasource',
        #                                     content_type=ct)
        # staff_group.permissions.add(permission)
        #
        # # Add staff users to staff_group
        # staff_1 = UserModel.objects.get(username='staff_1')
        # staff_2 = UserModel.objects.get(username='staff_2')
        # staff_2.user_permissions.add(permission)
        # staff_group.user_set.add(staff_1, staff_2)

    def login_superuser(self):
        self.login('superuser', 'super')

    def login_staff_1(self):
        self.login('staff_1', 'staff')

    def login_staff_2(self):
        self.login('staff_2', 'staff')

    def login(self, username, password):
        self.assertTrue(
            self.client.login(username=username, password=password)
        )

    def logout(self):
        self.client.logout()
