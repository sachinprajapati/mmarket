from django.db import models
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

def directory_path(instance, filename):
    return '{0}/{1}/{2}'.format(instance._meta.db_table.split('_')[1], instance.get_slug(), filename)

class Banner(models.Model):
    img = models.ImageField(upload_to=directory_path)
    caption = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='caption')
    order = models.PositiveSmallIntegerField(verbose_name=_("Display Order"))

    def get_slug(self):
        return self.slug

    def get_update_url(self):
        return reverse_lazy("update_banner", kwargs={'pk': self.pk})
