import os
import io
import json
import shutil
from PIL import Image as GenerateImage

from django.test import override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status

from .models import Category, Product, Image


User = get_user_model()
TEST_DIR = 'test_data'
def generate_photo_file(file_name='test'):
    file = io.BytesIO()
    image = GenerateImage.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = file_name + '.png'
    file.seek(0)
    return file


class CategoryCreateTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('category-create')
        self.user = User.objects.create(username='admin', password='admin', is_staff=True) #create admin user


    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_category_creation(self):
        self.authenticate()
        sample_category = {
            'title': 'first cat',
            'avatar': generate_photo_file(file_name='test')
        }
        response = self.client.post(self.url, sample_category)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        category = Category.objects.last()
        self.assertTrue(os.path.exists(category.avatar.path)) #test avatar file exist


class CategoryListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='admin', password='admin', is_staff=True) #create admin user
        self.url = reverse('category-list')

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_list_categories(self):
        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, []) #there is nothing in category


class CategoryUpdateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='admin', password='admin', is_staff=True) #create admin user
        self.category = Category.objects.create(
            title='first cat',
        )
        self.url = reverse('category-update', kwargs={'pk': self.category.id})

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_update_categories(self):
        self.authenticate()
        sample_category = {
            'title': 'second cat',
        }

        response = self.client.put(self.url, data=json.dumps(sample_category), content_type='application/json')
        self.assertNotEqual(response.data['title'], self.category.title)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CategoryDeleteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='admin', password='admin', is_staff=True) #create admin user
        self.category = Category.objects.create(
            title='first cat',
        )
        self.url = reverse('category-delete', kwargs={'pk': self.category.id})

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_Delete_categories(self):
        self.authenticate()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductCreateTestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title='first cat',
        )
        self.url = reverse('product-create')
        self.user = User.objects.create(username='admin', password='admin', is_staff=True) #create admin user
        self.user.save()
    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_product_creation(self):
        self.authenticate()
        sample_product = {
            'name': 'first pro',
            'selected_categories': [self.category.id],
            'avatar': generate_photo_file(file_name='test'),
            'uploaded_images': [generate_photo_file(file_name='test2')]
        }
        response = self.client.post(self.url, sample_product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product = Product.objects.last()
        self.assertTrue(os.path.exists(product.images.first().image.path)) #test product image file exists
        self.assertTrue(os.path.exists(product.avatar.path)) #test avatar file exists


class ProductListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='admin', password='admin', is_staff=True) #create admin user
        self.url = reverse('product-list')
    def authenticate(self):
        self.client.force_authenticate(user=self.user)
    def test_list_products(self):
        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0) #there is nothing in product


class ProductUpdateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='admin', password='admin', is_staff=True) #create admin user
        self.user.save()
        self.category = Category.objects.create(
            title='first cat',
        )
        self.product = Product.objects.create(
            name='first product',
            user_id=self.user.id,
        )
        self.product.categories.set([self.category.id])

        self.url = reverse('product-update', kwargs={'pk': self.product.id})

    def authenticate(self):
        self.client.force_authenticate(user=self.user)
    def test_update_product(self):
        self.authenticate()
        sample_product = {
            'name': 'updated product',
            'selected_categories': [self.category.id]
        }

        response = self.client.put(self.url, data=json.dumps(sample_product), content_type='application/json')
        self.assertNotEqual(response.data['name'], self.product.name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProductDeleteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='admin', password='admin', is_staff=True) #create admin user
        self.user.save()
        self.category = Category.objects.create(
            title='first cat',
        )
        self.product = Product.objects.create(
            name='first product',
            user_id=self.user.id,
        )
        self.product.categories.set([self.category.id])
        self.url = reverse('category-delete', kwargs={'pk': self.category.id})

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_Delete_categories(self):
        self.authenticate()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


def tearDownModule():
    print('Deleting temporary files...')
    shutil.rmtree(TEST_DIR, ignore_errors=True)

