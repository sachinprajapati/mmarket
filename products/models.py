from django.db import models
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from django.utils.safestring import mark_safe
from django.utils.html import escape

from djrichtextfield.models import RichTextField

def directory_path(instance, filename):
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

    def get_update_url(self):
        return reverse_lazy('update_product_class', kwargs={'pk': self.pk})

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

    def get_field(self):
        html = '<input type="%s" name="%s" class="form-control" required>'
        if self.type == 'text':
            return mark_safe(html % (self.type, self.id))
        if self.type == 'integer':
            return mark_safe(html % ('number', self.id))

class ProductAttributeValue(models.Model):
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE,verbose_name=_("Attribute"))
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='attribute_values', verbose_name=_("Product"))
    value_text = models.TextField(_('Text'), blank=True, null=True)
    value_integer = models.IntegerField(_('Integer'), blank=True, null=True, db_index=True)
    value_boolean = models.BooleanField(_('Boolean'), null=True, db_index=True)
    value_float = models.FloatField(_('Float'), blank=True, null=True, db_index=True)
    value_date = models.DateField(_('Date'), blank=True, null=True, db_index=True)
    value_datetime = models.DateTimeField(_('DateTime'), blank=True, null=True, db_index=True)

from datetime import date

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

    def get_discount_url(self):
        return reverse_lazy('create_discount', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse_lazy('update_products', kwargs={'pk': self.pk})

    def get_price(self):
        today = date.today()
        pd = ProductDiscount.objects.filter(models.Q(product=self, fdate__lte=today) & models.Q(models.Q(ldate__isnull=True) | models.Q(ldate__gte=today))).aggregate(discount=models.Sum('price'))
        return pd['discount'] if pd['discount'] else self.price

    def get_stock_url(self):
        if not hasattr(self, 'stockrecord'):
            return mark_safe('<a href="%s"><button class="btn btn-info btn-sm shadow-sm" style="background:#41cef1;border:none;"><span class="fa fa-plus"></span></button></a>' % escape(reverse_lazy('product_stock', kwargs={'pk': self.pk})))
        else:
            return mark_safe('<a href="%s"><button class="btn btn-light btn-sm shadow-sm"><span class="fa fa-pencil-alt"></span></button></a>' % escape(reverse_lazy('update_stock', kwargs={'pk': self.stockrecord.pk})))

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
    num_allocated = models.IntegerField(
        _("Number allocated"), default=0)
    low_stock_threshold = models.PositiveIntegerField(
        _("Low Stock Threshold"), blank=True, null=True)
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True,
                                        db_index=True)

    def get_available(self, n):
        return (self.num_in_stock-self.num_allocated)>=n

from datetime import date

class ProductDiscount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(verbose_name=_("Discounted Price"))
    fdate = models.DateField(default=date.today, verbose_name='From Date')
    ldate = models.DateField(null=True, blank=True, verbose_name='End Date')
    dt = models.DateTimeField(auto_now_add=True)

    def get_update_url(self):
        return reverse_lazy('update_discount', kwargs={'pk': self.pk})