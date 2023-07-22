from django.db import models
from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import User
from django.conf import settings




class Category(models.Model):
    parent = models.ForeignKey('self', verbose_name=_('parent'), blank=True, null=True, on_delete=models.CASCADE, related_name='children')
    title = models.CharField(verbose_name=_('title name'), max_length=50)
    avatar = models.ImageField(blank=True, upload_to='categories')
    is_enable = models.BooleanField(verbose_name=_('is enable'), default=True)
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)
    class Meta:
        db_table = 'categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    def __str__(self):
        return format(self.title)

class Product(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=50)
    description = models.TextField(verbose_name=_('description'), blank=True)
    avatar = models.ImageField(blank=True, upload_to='products')
    # is_enable = models.BooleanField(verbose_name=_('is enable'), default=True)
    price = models.FloatField(blank=True, null=True)
    slug = models.SlugField(default=None, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    number_of_sold = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', verbose_name=_('categories'))
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey('Product', related_name='images', verbose_name=_('product'), on_delete=models.CASCADE)
    image = models.ImageField(_('image'), upload_to='products/img/')
    # is_enable = models.BooleanField(verbose_name=_('is enable'), default=True)
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        db_table = 'images'
        verbose_name = _('image')
        verbose_name_plural = _('images')


