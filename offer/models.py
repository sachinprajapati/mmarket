from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from products.models import Category

DISCOUNT_TYPE = [
    (1, 'Pecentage'),
    (2, 'Flat')
]

SITE, VOUCHER, USER, SESSION = ("Site", "Voucher", "User", "Session")
TYPE_CHOICES = (
    (SITE, _("Site offer - available to all users")),
    (VOUCHER, _("Voucher offer - only available after entering "
                "the appropriate voucher code")),
    (USER, _("User offer - available to certain types of user")),
    (SESSION, _("Session offer - temporary offer, available for "
                "a user for the duration of their session")),
)

APPLICABLE_ON = [
    (1, _("MRP")),
    (2, _("Selling Price"))
]

class Coupon(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=25)
    discount_type = models.IntegerField(choices=DISCOUNT_TYPE, verbose_name=_("Discount Type"))
    total_discount = models.PositiveSmallIntegerField()
    offer_type = models.CharField(
        _("Type"), choices=TYPE_CHOICES, default=SITE, max_length=128)
    min_order = models.PositiveIntegerField(null=True, blank=True)
    applicable_on = models.PositiveSmallIntegerField(choices=APPLICABLE_ON, verbose_name=_("Applicable on Price"))
    max_user_applications = models.PositiveIntegerField(
        _("Max user applications"),
        help_text=_("The number of times a single user can use this offer"),
        blank=True, null=True)
    on_category = models.ManyToManyField(Category, blank=True,
                 help_text=_("Select category to avail. "
                             "Leave this empty to select all category.")
                 )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    start_datetime = models.DateField(
        _("Start date"), blank=True, null=True,
        help_text=_("Offers are active from the start date. "
                    "Leave this empty if the offer has no start date."))
    end_datetime = models.DateField(
        _("End date"), blank=True, null=True,
        help_text=_("Offers are active until the end date. "
                    "Leave this empty if the offer has no expiry date."))

    def get_update_url(self):
        return reverse_lazy('coupon_update', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse_lazy('coupon_detail', kwargs={'pk': self.pk})
