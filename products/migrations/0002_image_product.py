# Generated by Django 3.2 on 2023-07-22 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('avatar', models.ImageField(blank=True, upload_to='products')),
                ('price', models.FloatField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, default=None, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('number_of_sold', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('categories', models.ManyToManyField(to='products.Category', verbose_name='categories')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/img/', verbose_name='image')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'db_table': 'images',
            },
        ),
    ]
