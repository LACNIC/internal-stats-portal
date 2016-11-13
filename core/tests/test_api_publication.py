from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib import auth

from .utils import FixtureTestCase


class PublicationAPIListTestCase(FixtureTestCase):
    view_name = 'api-publications-list'

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

    def test_superuser_publications(self):
        url = reverse(self.view_name)

        self.login_superuser()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # POST
        new_data = {'name': 'rest publication', 'description': 'this is a desc',
                    'programming_language': 'python', 'update_value': 15,
                    'update_type': 'days', 'creator': 17,
                    'server_path': 'http://example.com',
                    'file_path': '/home/superuser', 'publishable': False,
                    'created': '2016-11-01T21:52:00-03:00',
                    'modified': '2016-11-11T22:53:00-03:00',
                    'data_sources': [5],
                    'responsibles': [18], 'databases': [4], 'tags': [7]}

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
        updated_field = {'name': 'a new name'}

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

    def test_staff_publications(self):
        url = reverse(self.view_name)

        self.login_staff_1()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # POST
        new_data = {'name': 'rest publication', 'description': 'this is a desc',
                    'programming_language': 'python', 'update_value': 15,
                    'update_type': 'days', 'server_path': 'http://example.com',
                    'file_path': '/home/staff', 'publishable': False,
                    'created': '2016-11-01T21:52:00-03:00',
                    'modified': '2016-11-11T22:53:00-03:00',
                    'data_sources': [5],
                    'responsibles': [18], 'databases': [4], 'tags': [7]}

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
        updated_field = {'name': 'a new name'}

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

    def test_staff_autopopulate_creator_publications(self):
        url = reverse(self.view_name)

        self.login_staff_1()

        # POST
        new_data = {'name': 'rest publication', 'description': 'this is a desc',
                    'programming_language': 'python', 'update_value': 15,
                    'update_type': 'days', 'server_path': 'http://example.com',
                    'file_path': '/home/staff', 'publishable': False,
                    'created': '2016-11-01T21:52:00-03:00',
                    'modified': '2016-11-11T22:53:00-03:00',
                    'data_sources': [5],
                    'responsibles': [18], 'databases': [4], 'tags': [7]}

        response = self.client.post(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # GET
        detail_view_name = 'api-publications-detail'
        url = reverse(detail_view_name,
                      kwargs={'pk': response.data['id']})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = auth.get_user(self.client)
        self.assertEqual(response.data['creator'], user.pk)


class PublicationAPIDetailTestCase(FixtureTestCase):
    view_name = 'api-publications-detail'

    def test_guest(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.publication_1_data['id']})

        self.logout()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

        # POST
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

        # PUT
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

        # PATCH
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_superuser_publications(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.publication_1_data['id']})

        self.login_superuser()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.publication_1_data)

        # POST
        updated_field = {'name': 'a new name'}

        new_data = self.publication_1_data.copy()
        new_data.update(updated_field)

        response = self.client.post(url, updated_field, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # PATCH
        response = self.client.patch(url, updated_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, new_data)

        # PUT
        new_data = {'name': 'pub replaced', 'description': 'this is a desc',
                    'programming_language': 'go', 'update_value': 30,
                    'update_type': 'days', 'creator': 18,
                    'server_path': 'http://example.com',
                    'file_path': '/home/superuser', 'publishable': False,
                    'created': '2016-11-01T21:52:00-03:00',
                    'modified': '2016-11-12T22:53:00-03:00',
                    'data_sources': [],
                    'responsibles': [18], 'databases': [], 'tags': [7]}

        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_data['id'] = self.publication_1_data['id']
        self.assertEqual(response.data, new_data)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_publications(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.publication_1_data['id']})

        self.login_staff_1()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.publication_1_data)

        # POST
        updated_field = {'name': 'a new name'}

        new_data = self.publication_1_data.copy()
        new_data.update(updated_field)

        response = self.client.post(url, updated_field, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # PATCH
        response = self.client.patch(url, updated_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # PUT
        new_data = {'name': 'pub replaced', 'description': 'new desc',
                    'programming_language': 'go', 'update_value': 20,
                    'update_type': 'months',
                    'server_path': 'http://example2.com',
                    'file_path': '/home/staff', 'publishable': True,
                    'created': '2016-11-02T21:52:00-03:00',
                    'modified': '2016-11-12T22:53:00-03:00',
                    'data_sources': [], 'responsibles': [18],
                    'databases': [], 'tags': [8]}

        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_edit_restriction_publications(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.publication_1_data['id']})

        # PATCH
        # Superuser
        self.login_superuser()
        updated_field = {'name': 'a new name'}
        response = self.client.patch(url, updated_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logout()
        # Staff_1
        self.login_staff_1()
        updated_field = {'name': 'another name'}
        response = self.client.patch(url, updated_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logout()
        # Staff_2
        self.login_staff_2()
        updated_field = {'name': 'this will fail!'}
        response = self.client.patch(url, updated_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.logout()

        # PUT
        # Superuser
        self.login_superuser()
        new_data = {'name': 'pub replaced', 'description': 'new desc',
                    'programming_language': 'go', 'update_value': 20,
                    'update_type': 'months', 'creator': 18,
                    'server_path': 'http://example2.com',
                    'file_path': '/home/staff', 'publishable': True,
                    'created': '2016-11-02T21:52:00-03:00',
                    'modified': '2016-11-12T22:53:00-03:00',
                    'data_sources': [], 'responsibles': [18],
                    'databases': [], 'tags': [8]}
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logout()
        # Staff_1
        self.login_staff_1()
        new_data = {'name': 'pub replaced', 'description': 'new desc',
                    'programming_language': 'go', 'update_value': 20,
                    'update_type': 'months',
                    'server_path': 'http://example2.com',
                    'file_path': '/home/staff', 'publishable': True,
                    'created': '2016-11-02T21:52:00-03:00',
                    'modified': '2016-11-12T22:53:00-03:00',
                    'data_sources': [], 'responsibles': [18],
                    'databases': [], 'tags': [8]}
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logout()
        # Staff_2
        self.login_staff_2()
        new_data = {'name': 'pub replaced', 'description': 'new desc',
                    'programming_language': 'go', 'update_value': 20,
                    'update_type': 'months',
                    'server_path': 'http://example2.com',
                    'file_path': '/home/staff', 'publishable': True,
                    'created': '2016-11-02T21:52:00-03:00',
                    'modified': '2016-11-12T22:53:00-03:00',
                    'data_sources': [], 'responsibles': [18],
                    'databases': [], 'tags': [8]}
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.logout()

    def test_staff_delete_restriction_publications(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.publication_1_data['id']})

        self.login_staff_2()

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # No podes enviar la informacion del creador cuando no sos superuser
        # Te tiene que tomar el creador como el propio usuario logueado si no sos superuser
        # enviar publicaciones con menos attrs de los necesarios
