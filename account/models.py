# account/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from urllib.parse import quote
from django.conf import settings


# -----------------------------
# StripeModel (unchanged)
# -----------------------------
class StripeModel(models.Model):
    email = models.EmailField(null=True, blank=True)
    name_on_card = models.CharField(max_length=200, null=True, blank=True)
    customer_id = models.CharField(max_length=200, blank=True, null=True)
    card_number = models.CharField(max_length=16, unique=True, null=True, blank=True)
    exp_month = models.CharField(max_length=2, validators=[RegexValidator(r'^\d{0,9}$')], null=True, blank=True)
    exp_year = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{0,9}$')], null=True, blank=True)
    card_id = models.TextField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, related_name="stripemodel", on_delete=models.CASCADE, null=True, blank=True)
    address_city = models.CharField(max_length=120, null=True, blank=True)
    address_country = models.CharField(max_length=120, null=True, blank=True)
    address_state = models.CharField(max_length=120, null=True, blank=True)
    address_zip = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{0,9}$')], null=True, blank=True)

    def __str__(self):
        return self.email or "stripe"


# -----------------------------
# BillingAddress (unchanged)
# -----------------------------
class BillingAddress(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    user = models.ForeignKey(User, related_name="billingmodel", on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        null=False,
        blank=False
    )
    pin_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{0,9}$')], null=False, blank=False)
    house_no = models.CharField(max_length=300, null=False, blank=False)
    landmark = models.CharField(max_length=120, null=False, blank=False)
    city = models.CharField(max_length=120, null=False, blank=False)
    state = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.name


# -----------------------------
# OrderModel (extended for COD + WhatsApp)
# -----------------------------
class OrderModel(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("PAID", "Paid"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]
    PAYMENT_CHOICES = [
        ("COD", "Cash on Delivery"),
        ("CARD", "Card"),
        ("OTHER", "Other"),
    ]

    # legacy / existing fields (kept for compatibility)
    name = models.CharField(max_length=120)
    ordered_item = models.CharField(max_length=200, null=True, blank=True, default="Not Set")
    card_number = models.CharField(max_length=16, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    paid_status = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # new fields
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="COD")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    items = models.JSONField(default=list, blank=True)  # [{id,name,qty,price,image?}, ...]

    customer_name = models.CharField(max_length=120, blank=True, default="")
    phone = models.CharField(max_length=32, blank=True, default="")
    city = models.CharField(max_length=120, blank=True, default="")
    notes = models.TextField(blank=True, default="")

    whatsapp_to = models.CharField(max_length=32, blank=True, default="")  # e.g. "2126XXXXXXXX" (no '+')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} — {self.user.username if self.user_id else 'guest'}"

    def build_whatsapp_text(self):
        lines = [
            f"📦 Nouvelle demande COD — Commande #{self.id}",
            f"👤 {self.customer_name or self.name}",
            f"📞 {self.phone or '-'}",
            f"🏠 {self.address or '-'}{(' — ' + self.city) if self.city else ''}",
            f"📝 Notes : {self.notes or '-'}",
            "",
            "🛒 Articles :",
        ]
        if self.items:
            for it in self.items:
                n = it.get("name", "Article")
                q = it.get("qty", 1)
                p = it.get("price", 0)
                lines.append(f"• {n} x{q} — {p} MAD")
        else:
            lines.append(f"• {self.ordered_item or 'Article'}")

        lines += ["", f"Total : {self.total_price or 0} MAD", "", "Merci de confirmer la commande 🙏"]
        return "\n".join(lines)

    def build_whatsapp_url(self):
        phone = self.whatsapp_to or getattr(settings, "WHATSAPP_ADMIN", "")
        text = quote(self.build_whatsapp_text())
        if not phone:
            return f"https://wa.me/?text={text}"
        return f"https://wa.me/{phone}?text={text}"
