from django.db import models

# Create your models here.

class Product(models.Model):
    title=models.CharField(max_length=250)
    description=models.TextField()
    price=models.DecimalField(decimal_places=2,max_digits=5)
    image=models.FileField(upload_to='products/',blank=True,null=True)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.title
