from rest_framework import status
from django.core.urlresolvers import reverse

from .utils import FixtureTestCase


class UserAPIListTestCase(FixtureTestCase):
    view_name = 'api-users-list'

    def test_guest(self):
        url = reverse(self.view_name)

        self.client.logout()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # POST
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PATCH
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_users(self):
        url = reverse(self.view_name)

        self.login_superuser()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # POST
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # PUT
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # PATCH
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_users(self):
        url = reverse(self.view_name)

        self.login_staff_1()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # POST
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PATCH
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserAPIDetailTestCase(FixtureTestCase):
    view_name = 'api-users-detail'

    def test_guest(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.superuser_data['id']})

        self.logout()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # POST
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PATCH
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_users(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.superuser_data['id']})

        self.login_superuser()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.superuser_data)

        # POST
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # PATCH
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # PUT
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_users(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.superuser_data['id']})

        self.login_staff_1()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.superuser_data)

        # POST
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

        # PATCH
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
