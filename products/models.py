from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

def directory_path(instance, filename):
    print(instance, dir(instance._meta))
    return '{0}/{1}/{2}'.format(instance._meta.db_table.split('_')[1], instance.slug, filename)

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True ,related_name='children')
    img = models.ImageField(upload_to=directory_path)
    dt = models.DateTimeField(auto_now_add=True)

    class Meta:  
        constraints = [
	        models.UniqueConstraint(fields=['slug', 'parent'], name="_(Can't create category same as parent)")
	    ] 
        verbose_name_plural = "categories"     

    def __str__(self):                           
        full_path = [self.name]                  
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

# class Product(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL)
#     name = models.CharField(max_length=255)
#     title = models.SlugField()
#     price = models.PositiveIntegerField()
