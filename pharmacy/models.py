# pharmacy/models.py
from django.db import models

class Drug(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per unit")
    stock_quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10, help_text="Alert when stock drops below this")
    expiry_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.stock_quantity} in stock)"

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.reorder_level