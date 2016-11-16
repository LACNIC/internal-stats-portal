from rest_framework import status
from django.core.urlresolvers import reverse

from core.tests.utils import FixtureTestCase


class DataSourceAPIListTestCase(FixtureTestCase):
    view_name = 'api-datasources-list'

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

    def test_superuser_datasources(self):
        url = reverse(self.view_name)

        self.login_superuser()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # POST
        new_data = {'notes': 'this is a note'}

        response = self.client.post(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.data
        del (response_data['id'])

        self.assertEqual(response_data, new_data)

        # PUT
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # PATCH
        updated_field = {'notes': 'a new note'}

        response = self.client.patch(url, updated_field, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_datasources(self):
        url = reverse(self.view_name)

        self.login_staff_1()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # POST
        new_data = {'notes': 'this is a note'}

        response = self.client.post(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.data
        del (response_data['id'])

        self.assertEqual(response_data, new_data)

        # PUT
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PATCH
        updated_field = {'notes': 'a new note'}

        response = self.client.patch(url, updated_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DataSourceAPIDetailTestCase(FixtureTestCase):
    view_name = 'api-datasources-detail'

    def test_guest(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.datasource_1_data['id']})

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

    def test_superuser_datasources(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.datasource_1_data['id']})

        self.login_superuser()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.datasource_1_data)

        # POST
        updated_field = {'notes': 'a new note'}

        new_data = self.datasource_1_data.copy()
        new_data.update(updated_field)

        response = self.client.post(url, updated_field, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # PATCH
        response = self.client.patch(url, updated_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, new_data)

        # PUT
        new_data = {'notes': 'another note'}

        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_data['id'] = self.datasource_1_data['id']
        self.assertEqual(response.data, new_data)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_datasources(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.datasource_1_data['id']})

        self.login_staff_1()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.datasource_1_data)

        # POST
        updated_field = {'notes': 'a new note'}

        new_data = self.datasource_1_data.copy()
        new_data.update(updated_field)

        response = self.client.post(url, updated_field, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # PATCH
        response = self.client.patch(url, updated_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT
        new_data = {'notes': 'another note'}

        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
