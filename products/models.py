from django.db import models
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.urls import reverse_lazy

from PIL import Image

from djrichtextfield.models import RichTextField

def directory_path(instance, filename):
    print(instance, dir(instance._meta))
    return '{0}/{1}/{2}'.format(instance._meta.db_table.split('_')[1], instance.get_slug(), filename)

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True ,related_name='children')
    img = models.ImageField(upload_to=directory_path)
    dt = models.DateTimeField(auto_now_add=True)

    class Meta:  
        constraints = [
	        models.UniqueConstraint(fields=['slug', 'parent'], name="_(Can't create category same as parent)")
	    ] 
        verbose_name_plural = "categories"  

    def get_slug(self):
        return self.slug

    # def __str__(self):
    #     full_path = [self.name]
    #     k = self.parent
    #     while k is not None:
    #         full_path.append(k.name)
    #         k = k.parent
    #     return ' -> '.join(full_path[::-1])

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse_lazy('update_category', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('delete_categories"', kwargs={'pk': self.pk})

class ProductClass(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    require_shipping = models.BooleanField(default=False)
    track_stock = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.name

    @property
    def has_attributes(self):
        return self.attributes.exists()

class ProductAttribute(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    TEXT = "text"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    DATE = "date"
    DATETIME = "datetime"
    TYPE_CHOICES = (
        (TEXT, _("Text")),
        (INTEGER, _("Integer")),
        (BOOLEAN, _("True / False")),
        (FLOAT, _("Float")),
        (DATE, _("Date")),
        (DATETIME, _("Datetime")),
    )
    type = models.CharField(
        choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0],
        max_length=20, verbose_name=_("Type"))
    required = models.BooleanField(default=True)
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE)

    def __str__(self):
        return '{} code {} type {}'.format(self.name, self.code, self.get_type_display())

    @property
    def set_value(self):
        return getattr(self.productattributevalue, 'value_'+self.type)

class ProductAttributeValue(models.Model):
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE,verbose_name=_("Attribute"))
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='attribute_values', verbose_name=_("Product"))
    value_text = models.TextField(_('Text'), blank=True, null=True)
    value_integer = models.IntegerField(_('Integer'), blank=True, null=True, db_index=True)
    value_boolean = models.BooleanField(_('Boolean'), null=True, db_index=True)
    value_float = models.FloatField(_('Float'), blank=True, null=True, db_index=True)
    value_date = models.DateField(_('Date'), blank=True, null=True, db_index=True)
    value_datetime = models.DateTimeField(_('DateTime'), blank=True, null=True, db_index=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    title = AutoSlugField(populate_from='name')
    price = models.PositiveIntegerField(verbose_name=_("Selling Price"))
    is_public = models.BooleanField(_('Is public'), default=True, db_index=True, help_text=_("Show this product in search results and catalogue listings."))
    upc = models.CharField(verbose_name=_("UPC"), max_length=64, blank=True, null=True, unique=True, help_text=_("Universal Product Code (UPC) is an identifier for "
                    "a product which is not specific to a particular "
                    " supplier. Eg an ISBN for a book."))
    description = RichTextField(_('Description'), blank=True)
    product_class = models.ForeignKey(ProductClass, on_delete=models.SET_NULL, null=True, blank=True)
    attributes = models.ManyToManyField('ProductAttribute', through='ProductAttributeValue',
        verbose_name=_("Attributes"),
        help_text=_("A product attribute is something that this product may "
                    "have, such as a size, as specified by its class"))
    categories = models.ManyToManyField('Category', verbose_name=_("Categories"))
    mrp = models.FloatField(verbose_name=_("Product MRP"))
    rating = models.FloatField(_('Rating'), null=True, editable=False)
    date_created = models.DateTimeField(
        _("Date created"), auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField(
        _("Date updated"), auto_now=True, db_index=True)
    is_discountable = models.BooleanField(
        _("Is discountable?"), default=True, help_text=_(
            "This flag indicates if this product can be used in an offer "
            "or not"))

    def __str__(self):
        return '%s' % self.title

    @property
    def first_image(self):
        if self.images.all():
            return self.images.first().img.url

    def get_update_url(self):
        return reverse_lazy('update_products', kwargs={'pk': self.pk})

    def get_stock_url(self):
        if not hasattr(self, 'stockrecord'):
            print("in if")
            return mark_safe('<a href="%s"><span class="fa fa-plus"></span></a>' % escape(reverse_lazy('product_stock', kwargs={'pk': self.pk})))
        else:
            return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(reverse_lazy('update_stock', kwargs={'pk': self.stockrecord.pk})))

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_("Product"))
    img = models.ImageField(upload_to=directory_path, max_length=255)
    caption = models.CharField(_("Caption"), max_length=200, blank=True)

    #: Use display_order to determine which is the "primary" image
    display_order = models.PositiveIntegerField(
        _("Display order"), default=0, db_index=True,
        help_text=_("An image with a display order of zero will be the primary"
                    " image for a product"))
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)

    def get_slug(self):
        return self.product.title

    # def save(self, *args, **kwargs):
    #     instance = super(ProductImage, self).save(*args, **kwargs)
    #     image = Image.open(instance.img.path)
    #     image.save(instance.img.path, quality=20, optimize=True)
    #     return instance

class StockRecord(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    num_in_stock = models.PositiveIntegerField(
        _("Number in stock"))
    #: The amount of stock allocated to orders but not fed back to the master
    #: stock system.  A typical stock update process will set the
    #: :py:attr:`.num_in_stock` variable to a new value and reset
    #: :py:attr:`.num_allocated` to zero.
    num_allocated = models.IntegerField(
        _("Number allocated"), default=0)

    #: Threshold for low-stock alerts.  When stock goes beneath this threshold,
    #: an alert is triggered so warehouse managers can order more.
    low_stock_threshold = models.PositiveIntegerField(
        _("Low Stock Threshold"), blank=True, null=True)
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True,
                                        db_index=True)

    def get_available(self, n):
        return (self.num_in_stock-self.num_allocated)>=n