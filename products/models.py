from django.db import models
from django.utils.translation import ugettext_lazy as _



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
