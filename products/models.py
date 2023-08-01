from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .validators import FileMimeValidator
import os

from django.db import models
from django.dispatch import receiver



class Category(models.Model):

    parent = models.ForeignKey('self', verbose_name=_('parent'), blank=True, null=True, on_delete=models.CASCADE, related_name='children')
    title = models.CharField(verbose_name=_('title name'), max_length=50, unique=True)
    avatar = models.ImageField(blank=True, upload_to='categories', validators=[FileMimeValidator()])
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
    avatar = models.ImageField(blank=True, upload_to='products', validators=[FileMimeValidator()])
    price = models.FloatField(blank=True, default=0)
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
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        db_table = 'images'
        verbose_name = _('image')
        verbose_name_plural = _('images')

@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `Image` object is deleted.
    """
    if instance.image:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `Product` object is deleted.
    """
    if instance.avatar:
        if os.path.exists(instance.avatar.path):
            os.remove(instance.avatar.path)

@receiver(models.signals.pre_save, sender=Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Product` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Product.objects.get(pk=instance.pk).avatar
    except Product.DoesNotExist:
        return False

    if old_file:
        if os.path.exists(old_file.path):
            os.remove(old_file.path)




@receiver(models.signals.pre_save, sender=Category)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Category` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Category.objects.get(pk=instance.pk).avatar
    except Category.DoesNotExist:
        return False

    if old_file:
        if os.path.exists(old_file.path):
            os.remove(old_file.path)


@receiver(models.signals.post_delete, sender=Category)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `Category` object is deleted.
    """
    if instance.avatar:
        if os.path.exists(instance.avatar.path):
            os.remove(instance.avatar.path)
