from django.db import models
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _

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

    def __str__(self):                           
        full_path = [self.name]                  
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

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
    attribute = models.OneToOneField(ProductAttribute, on_delete=models.CASCADE,verbose_name=_("Attribute"))
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
    price = models.PositiveIntegerField()
    is_public = models.BooleanField(_('Is public'), default=True, db_index=True, help_text=_("Show this product in search results and catalogue listings."))
    upc = models.CharField(verbose_name=_("UPC"), max_length=64, blank=True, null=True, unique=True, help_text=_("Universal Product Code (UPC) is an identifier for "
                    "a product which is not specific to a particular "
                    " supplier. Eg an ISBN for a book."))
    description = models.TextField(_('Description'), blank=True)
    product_class = models.ForeignKey(ProductClass, on_delete=models.SET_NULL, null=True, blank=True)
    attributes = models.ManyToManyField('ProductAttribute', through='ProductAttributeValue',
        verbose_name=_("Attributes"),
        help_text=_("A product attribute is something that this product may "
                    "have, such as a size, as specified by its class"))
    categories = models.ManyToManyField('Category', verbose_name=_("Categories"))
    mrp = models.FloatField()
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
        return self.images.first().img.url

    # @property
    # def get_attribute(self):
    #     print(self.attributes.all().values('name', 'code', 'type'))
    #     print(self.attribute_values.all().values('attribute'))
    #     dc = {}
    #     for i in self.attribute_values.all():
    #         dc[]

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
