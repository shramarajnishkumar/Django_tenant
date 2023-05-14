from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=70)
    description = models.TextField()
    price = models.IntegerField()
    date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.product_name